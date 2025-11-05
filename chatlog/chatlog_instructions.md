# Chat Log Maintenance Instructions for Any LLM

This document defines the exact, repeatable protocol an LLM must follow to record, summarize, correct, and manage conversation logs in the `chatlog/` directory.

---
## 1. Directory & Core Files
- Root folder: `chatlog/`
- Required files:
  - `index.md` (Markdown table, newest entries first)
  - `transcript.md` (chronological full conversation summary, oldest first)
  - Per-response files: `YYYY-MM-DDThh-mm-ssZ-id-XXX-response.md`
  - This instructions file: `chatlog_instructions.md`
- All files live directly inside `chatlog/` (flat structure; no subfolders).

---
## 2. Entry Lifecycle Overview
1. User sends a Question (prompt).
2. Assistant responds.
3. LLM (maintainer) appends a new entry to `index.md` at the top (descending order by timestamp).
4. LLM creates/updates a full response file containing entire assistant response and required metadata.
5. LLM appends summary to `transcript.md` (chronological order, bottom append).

---
## 3. ID & Timestamp Rules
- IDs are sequential integers starting at 1, incrementing by 1 for each new Question/Response pair.
- Timestamp format: **ISO 8601 UTC**: `YYYY-MM-DDThh:mm:ssZ`.
- Use the assistant response time for the timestamp.
- File name timestamp MUST replace colons (`:`) with hyphens (`-`): `YYYY-MM-DDThh-mm-ssZ-id-XXX-response.md`.

Example: Timestamp `2025-11-05T14:32:01Z` with ID 42 → `2025-11-05T14-32-01Z-id-042-response.md`.

---
## 4. `index.md` Table Schema
Markdown table columns (order fixed):
```
| ID | Timestamp (UTC) | Question | Response (Summary) | Link | Tags | Hash |
```
Definitions:
- **ID**: Integer sequence.
- **Timestamp (UTC)**: ISO format.
- **Question**: Original user prompt (trimmed; line breaks collapsed to spaces; max 160 chars, append `…` if truncated).
- **Response (Summary)**: One-sentence AI-generated summary (≤200 chars) describing the response intent/content (NOT just first sentence copied; produce an abstract).
- **Link**: Relative Markdown link to the full response file: `[Full](YYYY-MM-DDThh-mm-ssZ-id-XXX-response.md)`.
- **Tags**: Comma-separated lowercase keywords (auto-infer from content). See Tag Policy (§8).
- **Hash**: Placeholder `HASH_PENDING` unless a hashing routine is available. If hashing implemented, use SHA256 over the full assistant response text.

Newest entries MUST be inserted directly below the header row so the table remains in descending order.

---
## 5. Full Response File Template
Each per-response file MUST follow this structure:
```
## Full Response (ID <ID>)
Timestamp: <ISO8601 UTC>
Tags: <tag1, tag2, ...>
Question:
<Original user question verbatim>

Summary:
<The same one-sentence summary used in index>

Full Response:
<Complete assistant response content>

Attachments:
<If any referenced file contents are included, list them here.>

Hash: <HASH_PENDING or SHA256>
```
Notes:
- Preserve original formatting of the assistant response, including lists and code blocks.
- If there are attachments (file contents), copy them verbatim in fenced code blocks beneath `Attachments:`. If none, write `None`.

---
## 6. `transcript.md` Format
- Title: `# Conversation Transcript (Backfilled)` (exists already) or `# Conversation Transcript` for ongoing updates.
- Append chronological entries at the end (oldest first, newest last).
- Entry Structure:
```
---
## ID <ID> (<Timestamp>)
Question: <User question verbatim>
Assistant Response: See `<filename>`.
```
- Do NOT summarize here; link to full response file.

---
## 7. Summarization Policy (Response Summary)
- Provide a concise, single sentence capturing the *purpose* or *outcome* of the assistant response.
- Avoid vague phrases like "Answered the question"; be specific.
- Max length: 200 characters. Trim gracefully without cutting words; append `…` only if absolutely needed.
- Must not contain line breaks.

Examples:
- BAD: "Answer about logging." → TOO VAGUE.
- GOOD: "Outlined automation steps for Markdown-based chat logging with index and per-response files."

---
## 8. Tag Policy
Auto-infer tags from user question and assistant response content. Use 1–5 tags. Allowed base vocabulary (extend if logical):
```
planning, architecture, logging, rag, retrieval, frontend, backend, testing, security, docs, pivot, setup, config, questions
```
Rules:
- Lowercase only.
- No spaces; use hyphen if multiword (e.g., `prompt-logging`).
- Order tags by relevance (most specific first). Do not duplicate.

---
## 9. Corrections & Overwrites
- If a correction to an existing response is requested referencing an ID, overwrite ONLY the full response file.
- Keep the same ID, timestamp should update to correction time, and update the corresponding row in `index.md` (replace summary + timestamp + hash placeholder).
- Do NOT create an archive copy unless explicitly asked.
- Add tag `correction` when a response is overwritten.

Overwrite Procedure:
1. Locate existing row in `index.md` by ID.
2. Replace Timestamp, Response (Summary), Tags (append `correction`), Hash.
3. Regenerate full response file content using template.
4. Append a note at end of Full Response file: `Correction applied at <new timestamp>.`
5. Transcript: Add a NEW transcript entry referencing same ID with note: `(Correction)`.

---
## 10. Hash Handling
- Placeholder: `HASH_PENDING`.
- If hashing is implemented later: compute SHA256 over the raw Full Response section (excluding metadata header) and replace placeholder in both files.

---
## 11. Validation Rules Before Write
- Ensure ID not reused unless correction flow.
- Ensure Markdown table pipes align (one leading and trailing pipe per row).
- Ensure summary sentence ends with a period unless it ends with code or a closing parenthesis.
- Ensure timestamp conforms exactly to regex: `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$`.

---
## 12. Error Handling
If the LLM cannot produce a valid summary (edge case):
- Use fallback: `Summary unavailable.` and tag `needs-review`.
If file write fails or inconsistent formatting detected (simulated by user request):
- Produce a remediation response describing what to fix; do not update index until resolved.

---
## 13. Retroactive Backfill
- For any prior conversation not logged: reconstruct entries in chronological order starting at ID 1.
- After backfill, ensure `index.md` is descending (newest at top).

---
## 14. Adding New Entries (Algorithm)
1. Read current `index.md` to find current highest ID.
2. Assign ID = highest ID + 1.
3. Capture user question verbatim.
4. Generate summary per §7.
5. Infer tags per §8.
6. Get current UTC timestamp.
7. Create filename using timestamp + ID.
8. Insert new row at top of table.
9. Create full response file with template.
10. Append transcript entry at bottom.

---
## 15. Non-Functional Guidelines
- Keep operations atomic: each new pair should update all three surfaces (`index.md`, response file, `transcript.md`).
- Avoid reflowing or altering previous rows except during corrections.
- Do not re-wrap table columns unnecessarily.

---
## 16. Prohibited Actions
- Do not delete existing rows.
- Do not renumber IDs.
- Do not store raw API keys or secrets; redact if accidentally included.
- Avoid multi-sentence summaries.

---
## 17. Example Row & File
**Index Row:**
```
| 42 | 2025-11-05T14:32:01Z | How do we hash responses? | Described SHA256 usage and placeholder update strategy. | [Full](2025-11-05T14-32-01Z-id-042-response.md) | logging,setup | HASH_PENDING |
```
**Response File Snippet:**
```
## Full Response (ID 42)
Timestamp: 2025-11-05T14:32:01Z
Tags: logging, setup
Question:
How do we hash responses?

Summary:
Described SHA256 usage and placeholder update strategy.

Full Response:
<full content here>

Attachments:
None

Hash: HASH_PENDING
```

---
## 18. Completion Criteria
A logging action is considered successful when:
- Row present at top of `index.md` with correct formatting.
- Response file exists and matches template.
- Transcript has chronological entry.
- Summary follows policy.
- Tags valid.

---
## 19. Extension Hooks (Future Optional)
Potential future enhancements (not currently implemented):
- Automatic hashing script.
- JSON mirror file for programmatic parsing.
- Tag frequency analytics.

---
## 20. Quick Checklist for Each New Entry
- [ ] Next ID chosen
- [ ] Timestamp generated
- [ ] Summary valid length & style
- [ ] Tags inferred & normalized
- [ ] Index row inserted at top
- [ ] Response file created
- [ ] Transcript appended
- [ ] Hash placeholder set

---
**Use this file verbatim as operational instructions for any LLM maintaining the chat log.**
