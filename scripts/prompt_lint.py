#!/usr/bin/env python3
"""Prompt governance lint script.

Checks each .prompt.md file in .github/prompts for required frontmatter fields:
id, name, version, owners, description.
Warns if risk_level missing for high-impact prompts (recommendation, metrics).
Fails (exit 1) if any required field missing.
"""
from __future__ import annotations

import pathlib
import sys

REQUIRED = {"id", "name", "version", "owners", "description"}
HIGH_IMPACT_NAMES = {"recommendation", "metrics-explainer", "qa"}
HIGH_RISK_LEVELS = {"high", "critical"}

def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    block = parts[1]
    data = {}
    for line in block.strip().splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            data[key.strip()] = val.strip().strip('"')
    return data

def main() -> int:
    prompt_dir = pathlib.Path('.github/prompts')
    missing = {}
    warnings = []
    for file in prompt_dir.glob('*.prompt.md'):
        content = file.read_text(encoding='utf-8')
        fm = parse_frontmatter(content)
        absent = REQUIRED - fm.keys()
        if absent:
            missing[file.name] = sorted(absent)
        name = fm.get('name', '')
        if name in HIGH_IMPACT_NAMES:
            rl = fm.get('risk_level')
            if not rl:
                warnings.append(f"{file.name}: missing risk_level for high-impact prompt")
            elif rl in HIGH_RISK_LEVELS and 'rationale' not in fm:
                warnings.append(f"{file.name}: missing rationale line for {rl} risk prompt")
    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(w)
    if missing:
        print("ERROR: Missing required fields:")
        for fname, fields in missing.items():
            print(f"  {fname}: {', '.join(fields)}")
        return 1
    print("Prompt lint passed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
