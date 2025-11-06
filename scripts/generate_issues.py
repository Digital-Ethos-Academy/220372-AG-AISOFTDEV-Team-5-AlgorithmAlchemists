"""Generate markdown issue stubs from BACKLOG.md tables."""
from __future__ import annotations
import re
from pathlib import Path

BACKLOG = Path("BACKLOG.md").read_text(encoding="utf-8")
sections = re.findall(r"## Functional Requirements(.*?)## Quality Gate Enhancements", BACKLOG, re.S)
output = []
if sections:
    rows = re.findall(r"\| (FR\d+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|", sections[0])
    for fr_id, title, summary, ac_ref, owner, status in rows:  # type: ignore[misc]
        if status.strip() != "DONE":
            output.append(f"### {fr_id}: {title.strip()}\nOwner: {owner}\nStatus: {status}\nSummary: {summary}\nAcceptance: {ac_ref}\n---\n")
Path("ISSUE_STUBS.md").write_text("\n".join(output) or "No pending FR issues", encoding="utf-8")
print("ISSUE_STUBS.md written")
