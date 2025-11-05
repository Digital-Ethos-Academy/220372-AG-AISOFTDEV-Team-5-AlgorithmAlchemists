#!/usr/bin/env python3
"""Validate PRD + instruction integrity for CI.
Exit non-zero on failure.
"""
import json, re, hashlib, sys
from pathlib import Path

SENTINEL = Path('.agent-context/index.json')
PRD_VERSION_RE = re.compile(r'^Version:\s*(\d+\.\d+\.\d+)', re.MULTILINE)

FAIL = 0

def fail(msg, code=1):
    global FAIL
    sys.stderr.write(msg + '\n')
    FAIL = max(FAIL, code)

if not SENTINEL.exists():
    fail('Missing sentinel .agent-context/index.json', 2)
else:
    idx = json.loads(SENTINEL.read_text(encoding='utf-8'))
    prd = Path(idx['prd_path'])
    if not prd.exists():
        fail(f'PRD missing: {prd}', 3)
    else:
        text = prd.read_text(encoding='utf-8')
        m = PRD_VERSION_RE.search(text)
        if not m:
            fail('PRD version line missing', 4)
        prd_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        recorded = idx['prd_hash']
        if recorded not in ('HASH_PENDING', prd_hash):
            fail(f'PRD hash mismatch recorded={recorded} actual={prd_hash}', 5)
    instr_list = idx.get('instruction_files', [])
    if instr_list:
        for f in instr_list:
            p = Path(f)
            if not p.exists():
                fail(f'Missing instruction file: {p}', 6)
            else:
                if not p.read_text(encoding='utf-8').strip():
                    fail(f'Empty instruction file: {p}', 7)
    else:
        # Optional mode: absence of instruction files is acceptable under unified PRD approach.
        pass

if FAIL:
    sys.exit(FAIL)
print('Context integrity validation passed.')
