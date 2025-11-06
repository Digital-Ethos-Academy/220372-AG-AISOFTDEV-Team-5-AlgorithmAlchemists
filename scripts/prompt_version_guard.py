#!/usr/bin/env python3
"""Prompt version guard.

Ensures any staged changes to .prompt.md files include a bumped `version` in frontmatter
compared to HEAD. Fails if unchanged or missing.
"""
from __future__ import annotations
import subprocess
import sys
import pathlib
import re
from typing import Dict

PROMPT_DIR = pathlib.Path('.github/prompts')
VERSION_RE = re.compile(r'^version:\s*(.+)$', re.IGNORECASE)


def get_staged_prompt_files() -> list[pathlib.Path]:
    try:
        out = subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True)
    except subprocess.CalledProcessError:
        return []
    files = []
    for line in out.splitlines():
        if line.startswith('.github/prompts/') and line.endswith('.prompt.md'):
            files.append(pathlib.Path(line))
    return files


def parse_frontmatter(path: pathlib.Path) -> Dict[str, str]:
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---'):
        return {}
    parts = text.split('---', 2)
    if len(parts) < 3:
        return {}
    block = parts[1]
    data: Dict[str, str] = {}
    for line in block.strip().splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            data[k.strip()] = v.strip().strip('"')
    return data


def get_head_version(path: pathlib.Path) -> str | None:
    try:
        content = subprocess.check_output(['git', 'show', f'HEAD:{path.as_posix()}'], text=True)
    except subprocess.CalledProcessError:
        return None  # new file
    fm = parse_frontmatter_from_text(content)
    return fm.get('version')


def parse_frontmatter_from_text(text: str) -> Dict[str, str]:
    if not text.startswith('---'):
        return {}
    parts = text.split('---', 2)
    if len(parts) < 3:
        return {}
    block = parts[1]
    data: Dict[str, str] = {}
    for line in block.strip().splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            data[k.strip()] = v.strip().strip('"')
    return data


def version_bumped(old: str | None, new: str | None) -> bool:
    if new is None:
        return False
    if old is None:
        return True  # new file must have version
    return new != old


def main() -> int:
    staged = get_staged_prompt_files()
    if not staged:
        print('Prompt version guard: no staged prompt changes.')
        return 0
    errors = []
    for path in staged:
        fm = parse_frontmatter(path)
        new_version = fm.get('version')
        old_version = get_head_version(path)
        if not version_bumped(old_version, new_version):
            errors.append(f"{path}: version not bumped (old={old_version}, new={new_version})")
        if 'risk_level' in fm and fm.get('risk_level') in {'high','critical'} and 'rationale' not in fm:
            errors.append(f"{path}: missing rationale for high/critical risk prompt")
    if errors:
        print('PROMPT VERSION GUARD FAIL:')
        for e in errors:
            print(' -', e)
        return 1
    print('Prompt version guard passed.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
