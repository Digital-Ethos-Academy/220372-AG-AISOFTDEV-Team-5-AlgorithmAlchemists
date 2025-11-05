# Agent Instruction Execution Order

This file defines the authoritative load and execution sequence for all agent instruction documents.
Agents MUST:
1. Read this file first.
2. Load each listed instruction file in the exact order listed below.
3. Halt with an error if any required file is missing.
4. Ignore any extra instruction files not listed here until this file is updated.
5. Treat all rules as cumulative unless an explicit OVERRIDES section appears in a later file.

Order (top → bottom = priority / base → specialized):
1. branching_instructions.md
2. agent-workflow.md
3. automation.md
4. integrity.md
5. chatlog.md
6. multi-agent-coordination.md

## Rationale
- Branching establishes structural traceability baseline.
- Workflow defines the lifecycle around prompts and branches.
- Automation layers exact Git/CI behaviors.
- Integrity enforces hashes, security scanning, and file presence invariants.
- Chatlog ensures logging protocol is always respected after structural/automation rules are known.
- Multi-agent coordination (placeholder) will define collaboration semantics later.

## Modification Rules
- Adding a new instruction file requires inserting it into the ordered list here.
- Do NOT renumber historical items; append or insert thoughtfully.
- If a new file supersedes rules, include a heading: `## OVERRIDES` specifying exactly what prior sections (file + subsection) it replaces.

## Error Conditions
Agents must raise an error and STOP if:
- Any listed file is missing.
- Duplicate filenames appear in this directory.
- A listed file has an empty body (after trimming whitespace).

## Resolution Hierarchy
If conflicting directives exist without an explicit OVERRIDES section:
1. Earlier file wins (precedence is by sequence above).
2. Agent must flag a conflict in its output.
3. Human must add an explicit OVERRIDES section in a later file to resolve.

## Future Extension
Multi-agent augmentations will be added to `multi-agent-coordination.md` and placed after all foundational rules.

## Attention Capsule (for future large models)
Load order fingerprint (filenames only):
branching_instructions.md | agent-workflow.md | automation.md | integrity.md | chatlog.md | multi-agent-coordination.md

Do NOT proceed if any element is absent.
