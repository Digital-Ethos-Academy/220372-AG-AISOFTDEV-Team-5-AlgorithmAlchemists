#!/usr/bin/env python3
"""Bootstrap agent context: loads PRD, instruction files, builds (stub) embeddings, outputs JSON summary.

Phase 1: Hash + structure only. Embedding vectors are placeholders until an embedding provider is configured.
"""
import json, hashlib, os, sys, argparse, re, sqlite3, time
from pathlib import Path

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
TOP_K = 6
SENTINEL_INDEX = Path('.agent-context/index.json')
EMBED_DB_PATH = Path('.agent-context/agent_context.db')
PRD_VERSION_REGEX = re.compile(r'^Version:\s*(\d+\.\d+\.\d+)', re.MULTILINE)
TIMESTAMP = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

secret_patterns = [r'API_KEY=', r'SECRET=', r'PRIVATE_KEY', r'-----BEGIN']

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def read_file(path: Path) -> str:
    try:
        return path.read_text(encoding='utf-8')
    except FileNotFoundError:
        sys.stderr.write(f"ERROR: Missing file {path}\n")
        sys.exit(2)

def chunk_text(text: str, size: int, overlap: int):
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + size)
        chunk = text[start:end]
        chunks.append(chunk)
        if end == len(text):
            break
        start = end - overlap
    return chunks

def ensure_db(db_path: Path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS chunks (id INTEGER PRIMARY KEY, source TEXT, idx INTEGER, content TEXT, vector TEXT)")
    conn.commit()
    return conn

def store_chunks(conn, source: str, chunks):
    cur = conn.cursor()
    cur.execute("DELETE FROM chunks WHERE source = ?", (source,))
    for i, c in enumerate(chunks):
        # vector placeholder
        cur.execute("INSERT INTO chunks (source, idx, content, vector) VALUES (?, ?, ?, ?)", (source, i, c, '[]'))
    conn.commit()


def scan_secrets(text: str, path: Path):
    for pattern in secret_patterns:
        if re.search(pattern, text):
            sys.stderr.write(f"SECURITY WARNING: Potential secret pattern '{pattern}' found in {path}\n")
            return False
    return True


def main():
    parser = argparse.ArgumentParser(description='Bootstrap PRD + instruction context.')
    parser.add_argument('--summary-out', default='agent_context_summary.json', help='Output JSON summary file path')
    args = parser.parse_args()

    if not SENTINEL_INDEX.exists():
        sys.stderr.write('ERROR: Sentinel index .agent-context/index.json missing.\n')
        sys.exit(2)

    index = json.loads(SENTINEL_INDEX.read_text(encoding='utf-8'))
    prd_path = Path(index['prd_path'])
    prd_text = read_file(prd_path)

    # Extract version
    m = PRD_VERSION_REGEX.search(prd_text)
    version = m.group(1) if m else None
    if not version:
        sys.stderr.write('ERROR: PRD version line missing (Version: X.Y.Z).\n')
        sys.exit(3)

    prd_hash = sha256_text(prd_text)
    # Hash mismatch check (index placeholder may be HASH_PENDING initially)
    if index['prd_hash'] not in ('HASH_PENDING', prd_hash):
        alert_file = Path('HASH_ALERT.md')
        alert_file.write_text(f"Hash mismatch detected at {TIMESTAMP}\nRecorded: {index['prd_hash']}\nActual: {prd_hash}\n", encoding='utf-8')
        sys.stderr.write('HASH MISMATCH: Created HASH_ALERT.md and halting.\n')
        sys.exit(4)

    # Secret scan
    if not scan_secrets(prd_text, prd_path):
        sys.stderr.write('ERROR: Secret pattern found in PRD. Halt.\n')
        sys.exit(5)

    instruction_files = [Path(p) for p in index.get('instruction_files', [])]
    instructions_content = {}
    # Instruction files are now optional; if list empty skip silently.
    for f in instruction_files:
        if not f.exists():
            sys.stderr.write(f'WARNING: Optional instruction file missing: {f} (continuing)\n')
            continue
        txt = read_file(f)
        if not txt.strip():
            sys.stderr.write(f'WARNING: Optional instruction file empty: {f} (continuing)\n')
            continue
        if not scan_secrets(txt, f):
            sys.stderr.write(f'WARNING: Potential secret pattern in optional instruction file: {f} (skipping)\n')
            continue
        instructions_content[str(f)] = txt

    # Chunking & (stub) embedding store
    conn = ensure_db(Path(index['embedding_store']))
    prd_chunks = chunk_text(prd_text, CHUNK_SIZE, CHUNK_OVERLAP)
    store_chunks(conn, 'PRD', prd_chunks)
    for f, txt in instructions_content.items():
        chunks = chunk_text(txt, CHUNK_SIZE, CHUNK_OVERLAP)
        store_chunks(conn, f, chunks)

    summary = {
        'timestamp': TIMESTAMP,
        'version': version,
        'prd_hash': prd_hash,
        'chunks_indexed': len(prd_chunks),
    'instruction_files': list(instructions_content.keys()),
        'top_k_stub': prd_chunks[:TOP_K],  # placeholder retrieval
        'status': 'ok'
    }

    Path(args.summary_out).write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary))

if __name__ == '__main__':
    main()
