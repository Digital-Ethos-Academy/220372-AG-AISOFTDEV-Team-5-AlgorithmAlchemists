#!/usr/bin/env python3
"""Secret scanning script.

Scans plaintext source files for common secret patterns.
Fails (exit 1) if any potential secret is detected.
Patterns include:
- AWS Access Key ID: AKIA[0-9A-Z]{16}
- GitHub Personal Access Token: ghp_[A-Za-z0-9]{36}
- Generic 'sk_live_' keys
- 40-hex SHA1-like tokens (potential sensitive key)
- JWT (3 dot-separated base64url segments)

Skip directories: .git, logs, __pycache__, node_modules, .venv, dist, build.
"""
from __future__ import annotations
import re
import sys
import pathlib

SKIP_DIRS = {".git", "logs", "__pycache__", "node_modules", ".venv", "dist", "build"}
EXTENSIONS = {".py", ".md", ".json", ".toml", ".js", ".ts", ".tsx", ".yml", ".yaml"}

PATTERNS = {
    "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "github_pat": re.compile(r"ghp_[A-Za-z0-9]{36}"),
    "sk_live": re.compile(r"sk_live_[A-Za-z0-9]{16,}"),
    "sha1_hex": re.compile(r"\b[a-fA-F0-9]{40}\b"),
    "jwt": re.compile(r"\b[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"),
}

MAX_FILE_SIZE = 500_000  # bytes


def scan_file(path: pathlib.Path) -> list[tuple[str, str]]:
    hits = []
    try:
        if path.stat().st_size > MAX_FILE_SIZE:
            return hits
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return hits
    for name, regex in PATTERNS.items():
        for match in regex.findall(text):
            # Basic heuristics: skip known non-secret placeholders
            if "example" in match.lower():
                continue
            masked = match[:6] + "..." + match[-4:]
            hits.append((name, masked))
    return hits


def main() -> int:
    root = pathlib.Path(".")
    findings = []
    for path in root.rglob("*"):
        if path.is_dir():
            if path.name in SKIP_DIRS:
                continue
            else:
                continue  # don't descend separately (rglob already handles)
        if path.suffix.lower() not in EXTENSIONS:
            continue
        rel = path.relative_to(root)
        # Skip coverage/lint artifacts
        if any(part.startswith("coverage") for part in rel.parts):
            continue
        file_hits = scan_file(path)
        for kind, masked in file_hits:
            findings.append((str(rel), kind, masked))
    if findings:
        print("SECRET SCAN FAILURES:")
        for fpath, kind, masked in findings:
            print(f" - {fpath}: {kind} => {masked}")
        print("If false positives, add explicit ignore mechanism (TODO: allowlist file).")
        return 1
    print("Secret scan passed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
