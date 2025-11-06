#!/usr/bin/env python3
"""License allowlist enforcement.

Invokes pip-licenses (must be installed) to obtain dependency licenses in JSON.
Fails (exit 1) if any license outside ALLOWLIST is detected.

Usage:
  python scripts/license_allowlist.py --allow MIT Apache-2.0 BSD-3-Clause ISC

Notes:
- Multiple licenses in a single package entry are split on ';' or ','.
- Non-classified licenses ("UNKNOWN") trigger failure.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from typing import Set

DEFAULT_ALLOW = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC"}


def fetch_licenses() -> list[dict]:
    try:
        proc = subprocess.run([
            sys.executable,
            "-m",
            "piplicenses",
            "--format",
            "json",
            "--with-urls",
            "--with-license-file",
        ], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("ERROR: pip-licenses invocation failed", e.stderr)
        sys.exit(2)
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        print("ERROR: Unable to parse pip-licenses JSON output")
        sys.exit(3)


def parse_package_licenses(raw: list[dict]) -> dict[str, Set[str]]:
    out: dict[str, Set[str]] = {}
    for pkg in raw:
        name = pkg.get("Name") or pkg.get("name")
        lic = pkg.get("License") or pkg.get("license") or "UNKNOWN"
        tokens = [t.strip() for chunk in lic.split(";") for t in chunk.split(",")]
        out[name] = {t for t in tokens if t}
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow", nargs="*", default=None, help="Override allowlist")
    args = parser.parse_args()

    allowlist = set(args.allow) if args.allow else DEFAULT_ALLOW
    data = fetch_licenses()
    mapping = parse_package_licenses(data)

    violations = {}
    for pkg, licenses in mapping.items():
        bad = [l for l in licenses if l not in allowlist]
        if bad or not licenses:
            violations[pkg] = bad or ["UNKNOWN"]

    if violations:
        print("LICENSE ALLOWLIST VIOLATIONS:")
        for pkg, lic in violations.items():
            print(f" - {pkg}: {', '.join(lic)}")
        print(f"Allowed: {', '.join(sorted(allowlist))}")
        return 1
    print("License allowlist passed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
