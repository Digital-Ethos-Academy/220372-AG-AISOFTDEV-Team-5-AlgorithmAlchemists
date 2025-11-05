#!/usr/bin/env python3
"""Populate instruction file hashes into docs/agent_instructions/index.json.
Run after any modification to instruction files.
"""
import json, hashlib, sys
from pathlib import Path

INDEX_PATH = Path('docs/agent_instructions/index.json')
INSTR_DIR = Path('docs/agent_instructions')

def sha256_path(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    if not INDEX_PATH.exists():
        sys.stderr.write('ERROR: index.json missing.\n')
        sys.exit(2)
    data = json.loads(INDEX_PATH.read_text(encoding='utf-8'))
    for entry in data.get('files', []):
        name = entry['name']
        fpath = INSTR_DIR / name
        if not fpath.exists():
            sys.stderr.write(f'ERROR: missing instruction file {name}\n')
            sys.exit(3)
        entry['hash'] = sha256_path(fpath)
    data['status'] = 'hashed'
    INDEX_PATH.write_text(json.dumps(data, indent=2), encoding='utf-8')
    print('Updated instruction file hashes.')

if __name__ == '__main__':
    main()
