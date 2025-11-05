"""Chat log turn writer.

Best-practice implementation based on project instructions in:
  - chatlog/chatlog_instructions.md
  - docs/RAG_Navigator_PRD.md

Features:
  * Add new turn (question + answer) with sequential ID.
  * Correction mode (overwrite existing ID row + file, append transcript correction entry).
  * Atomic writes (temp file -> rename) for index, transcript, response file, JSON mirror.
  * Concurrency guard via .chatlog.lock (timeout & stale lock recovery).
  * JSON mirror file (chatlog/index.json) for programmatic access.
  * Summary generation (≤200 chars, ends with period) & tag inference.
  * Hash placeholder (HASH_PENDING) with optional --hash to compute SHA256 over Full Response section.
  * Dry-run support.
  * Git stage optional (--git-stage) without committing (commit handled upstream).
  * Structured JSON status output to stdout.

Usage examples:
  echo '{"question":"What is the plan?","answer":"We will implement per-turn logging."}' | \
    python scripts/log_chat_turn.py --mode add

  echo '{"question":"Correction ID 5: Update answer","answer":"Revised details."}' | \
    python scripts/log_chat_turn.py --mode correction --id 5

Alternative file-based:
  python scripts/log_chat_turn.py --mode add --question-file q.txt --answer-file a.txt

Exit codes:
  0 success
  1 fatal error
  2 validation / formatting error
  3 correction applied (success variant)

NOTE: This script assumes repository root as CWD when run; adjust paths if needed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional

REPO_ROOT = Path(__file__).resolve().parents[1]
CHATLOG_DIR = REPO_ROOT / "chatlog"
INDEX_MD = CHATLOG_DIR / "index.md"
TRANSCRIPT_MD = CHATLOG_DIR / "transcript.md"
INSTRUCTIONS_MD = CHATLOG_DIR / "chatlog_instructions.md"
JSON_MIRROR = CHATLOG_DIR / "index.json"
LOCK_FILE = CHATLOG_DIR / ".chatlog.lock"
ERROR_FILE = CHATLOG_DIR / ".chatlog_error"

SUMMARY_MAX = 200
QUESTION_MAX = 160
LOCK_TIMEOUT_SECONDS = 120

ALLOWED_TAGS = {
    "planning","architecture","logging","rag","retrieval","frontend","backend","testing",
    "security","docs","pivot","setup","config","questions"
}

TIMESTAMP_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def utc_now_iso() -> str:
    return datetime.utcnow().replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def ensure_chatlog_dir():
    CHATLOG_DIR.mkdir(exist_ok=True)


def read_index_md() -> List[str]:
    if not INDEX_MD.exists():
        # Initialize with header.
        header = ["# Chat Log Index\n", "\n", "Newest first. Hash placeholders will be replaced once hashing script is added.\n", "\n",
                  "| ID | Timestamp (UTC) | Question | Response (Summary) | Link | Tags | Hash |\n",
                  "|----|-----------------|----------|--------------------|------|------|------|\n"]
        return header
    return INDEX_MD.read_text(encoding="utf-8").splitlines(keepends=True)


def parse_highest_id(lines: List[str]) -> int:
    highest = 0
    for line in lines:
        if line.startswith("|") and line.count("|") >= 7 and not line.startswith("| ID "):
            parts = [p.strip() for p in line.strip().split("|")][1:-1]
            try:
                curr_id = int(parts[0])
                if curr_id > highest:
                    highest = curr_id
            except ValueError:
                continue
    return highest


def infer_tags(question: str, answer: str) -> List[str]:
    text = f"{question} {answer}".lower()
    tags = []
    for tag in ALLOWED_TAGS:
        if tag in text:
            tags.append(tag)
    if not tags:
        tags = ["logging"]
    return tags[:5]


def generate_summary(answer: str) -> str:
    flat = normalize_whitespace(answer)
    if len(flat) <= SUMMARY_MAX:
        summary = flat
    else:
        # Truncate at last space before limit.
        cut = flat[:SUMMARY_MAX].rsplit(" ", 1)[0]
        summary = cut + "…"
    # Ensure single sentence style ends with period unless already ends with punctuation.
    if not summary.endswith(('.', '!', '?', '…')):
        summary += '.'
    return summary


def truncate_question(question: str) -> str:
    q = normalize_whitespace(question)
    if len(q) <= QUESTION_MAX:
        return q
    cut = q[:QUESTION_MAX].rsplit(" ", 1)[0]
    return cut + "…"


def acquire_payload(args) -> Dict[str, str]:
    if args.question_file and args.answer_file:
        question = Path(args.question_file).read_text(encoding="utf-8")
        answer = Path(args.answer_file).read_text(encoding="utf-8")
        return {"question": question, "answer": answer}
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw:
            try:
                obj = json.loads(raw)
                return {"question": obj["question"], "answer": obj["answer"]}
            except Exception as e:
                fatal_error(f"Invalid stdin JSON payload: {e}")
    fatal_error("No input provided. Use --question-file/--answer-file or pipe JSON to stdin.")


def fatal_error(message: str, code: int = 1, context: Optional[Dict[str, Any]] = None):
    ERROR_FILE.write_text(json.dumps({"error": message, "context": context or {}}, indent=2), encoding="utf-8")
    print(json.dumps({"status": "error", "message": message}, indent=2))
    sys.exit(code)


def establish_lock():
    now = time.time()
    if LOCK_FILE.exists():
        age = now - LOCK_FILE.stat().st_mtime
        if age > LOCK_TIMEOUT_SECONDS:
            # Stale lock; remove.
            LOCK_FILE.unlink(missing_ok=True)
        else:
            fatal_error("Another logging process is active (lock present).", code=2,
                        context={"lock_age_seconds": age})
    LOCK_FILE.write_text(str(now), encoding="utf-8")


def release_lock():
    if LOCK_FILE.exists():
        LOCK_FILE.unlink(missing_ok=True)


def write_atomic(path: Path, content: str):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def compute_hash(full_response_section: str) -> str:
    return hashlib.sha256(full_response_section.encode("utf-8")).hexdigest()


def build_response_file(id_: int, timestamp: str, tags: List[str], question: str, summary: str, answer: str, hash_value: str, correction: bool) -> str:
    lines = [
        f"## Full Response (ID {id_})\n",
        f"Timestamp: {timestamp}\n",
        f"Tags: {', '.join(tags)}\n",
        "Question:\n",
        f"{question}\n\n",
        "Summary:\n",
        f"{summary}\n\n",
        "Full Response:\n",
        f"{answer}\n\n",
        "Attachments:\n",
        "None\n\n",
        f"Hash: {hash_value}\n",
    ]
    if correction:
        lines.append(f"\nCorrection applied at {timestamp}.\n")
    return "".join(lines)


def extract_full_response_for_hash(response_file_content: str) -> str:
    # Hash only the actual assistant response text under 'Full Response:' until 'Attachments:'
    pattern = re.compile(r"Full Response:\n(.*?)\n\nAttachments:\n", re.DOTALL)
    m = pattern.search(response_file_content)
    return m.group(1).strip() if m else ""


def update_json_mirror(entries: List[Dict[str, Any]]):
    write_atomic(JSON_MIRROR, json.dumps(entries, indent=2))


def parse_index_entries(lines: List[str]) -> List[Dict[str, Any]]:
    entries = []
    for line in lines:
        if line.startswith("|") and line.count("|") >= 7 and not line.startswith("| ID "):
            parts = [p.strip() for p in line.strip().split("|")][1:-1]
            try:
                id_ = int(parts[0])
            except ValueError:
                continue
            timestamp, question, summary, link, tags, hash_value = parts[1:]
            entries.append({
                "id": id_,
                "timestamp": timestamp,
                "question": question,
                "summary": summary,
                "link": link[6:-1] if link.startswith("[Full](") else link,
                "tags": [t.strip() for t in tags.split(",") if t.strip()],
                "hash": hash_value,
            })
    # Already newest first per spec.
    return entries


def render_index(lines: List[str], new_row: Optional[str], correction_id: Optional[int], updated_row: Optional[str]) -> str:
    output = []
    header_inserted = False
    for line in lines:
        output.append(line)
        if not header_inserted and line.startswith("|----"):
            header_inserted = True
            if new_row:
                output.append(new_row)
    if correction_id and updated_row:
        # Replace the row for that ID.
        for i, line in enumerate(output):
            if line.startswith("|") and line.count("|") >= 7 and not line.startswith("| ID "):
                parts = [p.strip() for p in line.strip().split("|")][1:-1]
                try:
                    id_ = int(parts[0])
                except ValueError:
                    continue
                if id_ == correction_id:
                    output[i] = updated_row
                    break
    return "".join(output)


def append_transcript(transcript_content: str, id_: int, timestamp: str, question: str, filename: str, correction: bool) -> str:
    entry = ["---\n",
             f"## ID {id_} ({timestamp}){' (Correction)' if correction else ''}\n",
             f"Question: {question}\n",
             f"Assistant Response: See `{filename}`.\n"]
    if not transcript_content.endswith("\n"):
        transcript_content += "\n"
    return transcript_content + "".join(entry)


def main():
    parser = argparse.ArgumentParser(description="Log a chat turn (add or correction).")
    parser.add_argument("--mode", choices=["add", "correction"], required=True)
    parser.add_argument("--id", type=int, help="ID for correction mode")
    parser.add_argument("--question-file", help="Path to file containing question text")
    parser.add_argument("--answer-file", help="Path to file containing answer text")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--git-stage", action="store_true")
    parser.add_argument("--hash", action="store_true", help="Compute SHA256 hash now instead of HASH_PENDING")
    args = parser.parse_args()

    ensure_chatlog_dir()
    establish_lock()
    try:
        payload = acquire_payload(args)
        question_raw = payload["question"].strip()
        answer_raw = payload["answer"].strip()

        if args.mode == "correction" and not args.id:
            fatal_error("--id required for correction mode", code=2)

        index_lines = read_index_md()
        transcript_text = TRANSCRIPT_MD.read_text(encoding="utf-8") if TRANSCRIPT_MD.exists() else "# Conversation Transcript\n\n"

        existing_entries = parse_index_entries(index_lines)
        highest_id = parse_highest_id(index_lines)

        correction = args.mode == "correction"
        if correction and not any(e["id"] == args.id for e in existing_entries):
            fatal_error(f"Cannot correct: ID {args.id} not found", code=2)

        new_id = args.id if correction else highest_id + 1
        timestamp = utc_now_iso()
        q_display = truncate_question(question_raw)
        summary = generate_summary(answer_raw)
        tags = infer_tags(question_raw, answer_raw)
        rel_filename = f"{timestamp.replace(':','-')}-id-{new_id:03d}-response.md"
        response_path = CHATLOG_DIR / rel_filename

        # Build response file content first (hash may depend on it.)
        provisional_content = build_response_file(new_id, timestamp, tags, question_raw, summary, answer_raw, "HASH_PENDING", correction)
        hash_value = "HASH_PENDING"
        if args.hash:
            full_resp = extract_full_response_for_hash(provisional_content)
            if full_resp:
                hash_value = compute_hash(full_resp)
                provisional_content = provisional_content.replace("HASH_PENDING", hash_value, 1)

        # Build index row.
        row = f"| {new_id} | {timestamp} | {q_display} | {summary} | [Full]({rel_filename}) | {','.join(tags)} | {hash_value} |\n"
        updated_row = None
        if correction:
            updated_row = row
            row = None  # No prepend; we replace existing.

        rendered_index = render_index(index_lines, row, new_id if correction else None, updated_row)
        updated_transcript = append_transcript(transcript_text, new_id, timestamp, question_raw, rel_filename, correction)

        # Update JSON mirror (newest first already) after modification.
        new_entries = []
        # Re-parse final index content for mirror coherence.
        for line in rendered_index.splitlines():
            if line.startswith("|") and line.count("|") >= 7 and not line.startswith("| ID "):
                parts = [p.strip() for p in line.strip().split("|")][1:-1]
                try:
                    id_ = int(parts[0])
                except ValueError:
                    continue
                ts, q, summ, link, tag_str, hv = parts[1:]
                new_entries.append({
                    "id": id_,
                    "timestamp": ts,
                    "question": q,
                    "summary": summ,
                    "link": link[6:-1] if link.startswith("[Full](") else link,
                    "tags": [t for t in tag_str.split(",") if t],
                    "hash": hv
                })

        if args.dry_run:
            print(json.dumps({
                "status": "dry-run",
                "id": new_id,
                "timestamp": timestamp,
                "index_row": updated_row or row,
                "response_file": rel_filename,
                "tags": tags,
                "summary": summary,
                "hash": hash_value
            }, indent=2))
            release_lock()
            sys.exit(0)

        # Atomic writes.
        write_atomic(INDEX_MD, rendered_index)
        write_atomic(TRANSCRIPT_MD, updated_transcript)
        write_atomic(response_path, provisional_content)
        update_json_mirror(new_entries)

        if args.git_stage:
            # Best-effort staging; ignore failure.
            os.system(f"git add {CHATLOG_DIR.as_posix()}")

        print(json.dumps({
            "status": "ok" if not correction else "correction",
            "id": new_id,
            "timestamp": timestamp,
            "file": rel_filename,
            "tags": tags,
            "summary": summary,
            "hash": hash_value
        }, indent=2))
        release_lock()
        sys.exit(0 if not correction else 3)
    except SystemExit:
        # Already handled.
        pass
    except Exception as e:
        release_lock()
        fatal_error(f"Unhandled exception: {e}")


if __name__ == "__main__":
    main()
