# Branching Strategy & Operational Instructions

This document defines the branching model for the RAG Navigator project. It integrates prompt-based traceability (chatlog + prompt branches) with phased delivery outlined in the PRD.

---
## 1. Goals
- Maintain a clear, auditable lineage from every prompt (conversation entry) to version-controlled changes.
- Support phased development (planning → architecture → ingestion → retrieval → generation → frontend → testing → security → presentation).
- Keep workflow lightweight (avoid full GitFlow overhead) while retaining professional structure.
- Minimize merge conflicts in shared metadata files (chatlog/index.md, transcript.md, prompts/*).

Model: **Lightweight Hybrid** – a single main branch with:
- Long‑lived phase branches (one per major PRD phase).
- Short‑lived feature branches derived from phase branches or main.
- Mandatory prompt branches tying each meaningful prompt to a commit (or a no-op record if no file change).
- Optional daily logs/<date> branches (only if batching multiple pure logging updates makes sense; otherwise skip).

---
## 2. Branch Types & Naming Conventions
Always use kebab-case after prefix. Avoid uppercase.

| Type | Purpose | Naming Pattern | Lifespan |
|------|---------|----------------|----------|
| phase | Houses work for a major PRD phase | `phase/<phase-name>` | Until phase completion |
| feature | Implements a discrete functional slice | `feature/<slug>` | Short-lived (merge & delete) |
| prompt | Trace a single prompt’s artifact change | `prompt/<id>-<short-slug>` | Very short-lived |
| experiment | Exploratory spike | `experiment/<slug>` | Delete or archive quickly |
| docs | Documentation-only changes | `docs/<slug>` | Short-lived |
| fix | Hotfix / bug correction | `fix/<slug>` | Short-lived |
| logs (optional) | Batch non-code logging changes for a day | `logs/YYYY-MM-DD` | Same day |

### 2.1 Slug Rules
- Derive from the first 4–6 meaningful words of the prompt/question or feature description.
- Strip punctuation, convert spaces → hyphens.
- Keep ≤ 32 characters where possible (soft limit for readability).

### 2.2 Prompt Branch Creation Rule
Create a `prompt/<id>-<slug>` branch **only if** the prompt results in (a) new or changed file(s) OR (b) a logged intent that impacts future work. If purely conversational with no artifact: branch may be created with a no‑op commit (optional) — default: **still create** for consistency.

---
## 3. Phase Mapping
Phases (mirrors PRD):
- planning
- architecture
- ingestion
- retrieval
- generation
- frontend
- testing
- security
- presentation

Long-lived branches (create at first need):
```
phase/planning
phase/architecture
phase/ingestion
phase/retrieval
phase/generation
phase/frontend
phase/testing
phase/security
phase/presentation
```

Feature branches normally base off an active phase branch. Example:
`git checkout -b feature/retrieval-ranking phase/retrieval`

Prompt branches normally base off **current active phase branch** if that branch is ahead of main; otherwise base off main.

---
## 4. Branch Selection Decision Tree (Simplified)
1. Is this initiating/continuing a phase? → Use or create `phase/<phase>`.
2. Is this a discrete functional addition inside an active phase? → `feature/<slug>` (base: phase branch).
3. Is this user prompt requiring a logged change? → `prompt/<id>-<slug>` (base: active phase or main).
4. Is this purely docs? → `docs/<topic>`.
5. Is this an urgent fix on main? → `fix/<issue>`.
6. Exploratory? → `experiment/<slug>`.

---
## 5. Commit Message Format
Single commit per short-lived branch (feature/prompt/docs) unless iterative development is needed.

Template:
```
<type>(<phase>): <concise summary>

[prompt:<ID>] [tags:<tag1,tag2>] [hash:<SHA256|N/A>]

Details:
- Files: <comma-separated or count>
- Rationale: <short justification>
- Response: <if hash=N/A explain: e.g., "Response file N/A for reason">
```
Examples:
```
prompt(retrieval): Add hybrid rank merge function

[prompt:009] [tags:retrieval,ranking] [hash:N/A]
Details:
- Files: backend/app/retrieval.py
- Rationale: Implements merge scoring
- Response: Response file N/A for reason: initial stub no assistant full output yet
```

```
feature/frontend: Add dark mode toggle component

[prompt:014] [tags:frontend,ui] [hash:ab12c3...]
Details:
- Files: frontend/src/components/DarkModeToggle.jsx
- Rationale: Implements UX requirement
- Response: Included in full response file
```

---
## 6. Pull Requests & Merging
- **PR Required:** All branches (even prompt) to enforce consistent traceability.
- **Prompt Branches:** Fast-forward merge where possible; squash optional but generally avoid rewriting the single commit.
- **Feature / Phase:** Prefer squash when multiple commits; else fast-forward if linear.
- **Docs / Prompt Only:** Auto-merge allowed after automated lint/test pass.

PR Title Template:
```
[type][phase][prompt:<ID>] <summary>
```
PR Body Auto Sections:
- Summary
- Related Prompt ID & Link
- Changed Files
- Test/Verification Notes
- Risks / Rollback Plan

---
## 7. Conflict Resolution Policy
### 7.1 General Rule
- Rebase onto updated main or phase branch before PR merge.
- Resolve conflicts locally; do not rely on web UI auto merges for structured logs.

### 7.2 chatlog/index.md or transcript.md Conflicts
1. Checkout your branch.
2. `git fetch origin && git rebase origin/main` (or phase branch).
3. If conflict in `chatlog/index.md`:
   - Open the latest main version.
   - Insert your new row at correct descending position (top beneath header) referencing original timestamp.
   - Ensure table alignment & no duplicate ID.
4. Re-run (if available) hashing script to refresh `HASH_PENDING` if necessary.
5. Continue rebase: `git add chatlog/index.md && git rebase --continue`.
6. Force-push branch if needed: `git push --force-with-lease`.

If multiple prompt branches race: merge/FF them sequentially in time order (oldest first) to keep IDs stable.

---
## 8. Branch Lifecycle & Retention
| Branch Type | Delete After Merge? | Archive? | Tagging |
|-------------|---------------------|----------|---------|
| prompt | Yes (default) | No | None |
| feature | Yes | Optional: add to `branch_archive.md` | None |
| phase | No (until phase completion) | Tag completion | Tag: `phase-<phase>-complete` |
| docs | Yes | No | None |
| fix | Yes | No | None |
| experiment | Yes (unless converted) | Optional | None |

Archive File (optional future): `docs/branch_archive.md` listing retired feature branches.

---
## 9. Tagging & Phase Completion
When a phase is complete (e.g., architecture):
```
git checkout main
git merge --ff-only phase/architecture
git tag phase-architecture-complete
```
Then optionally delete the phase branch if no further work: `git branch -d phase/architecture`.

---
## 10. Automation Scripts (Planned Placeholders)
Placed later in `scripts/` (not yet implemented):
- `new_branch.py`: Given prompt ID + slug + type + phase → creates branch, updates index if needed.
- `merge_prompt_branch.py`: Runs tests → merges prompt branch (fast-forward) → deletes branch → updates optional branch index.
- `pre_commit_check.py`: Verifies `.env` not staged and warns on secrets.

Script environment assumptions: Python 3.11+, git CLI available.

---
## 11. Security & Hygiene
- `.env` must remain untracked; confirm with `git ls-files .env` → expect no output.
- Add a pre-commit hook (future) to block commits containing patterns: `API_KEY=`, `SECRET=`, `-----BEGIN`.
- Avoid embedding API responses containing proprietary data directly; summarize instead.

---
## 12. Prompt Branch Flow (End-to-End)
1. Log prompt in chatlog (ID assigned).
2. Derive slug: words 1–5 of question.
3. `git checkout -b prompt/<id>-<slug> <base>` (base = active phase or main).
4. Apply changes (docs/code/tests).
5. Compute or set `HASH_PENDING`.
6. Commit with template.
7. Open PR (title includes `[prompt:<id>]`).
8. If only docs/log updates → CI passes → auto fast-forward merge.
9. Delete branch locally & remote: `git push origin --delete prompt/<id>-<slug>`.

---
## 13. Decision Matrix for Base Branch
| Scenario | Base Branch |
|----------|-------------|
| New phase initiated | main |
| Feature within active phase | phase/<phase> |
| Prompt referencing ongoing phase | phase/<phase> |
| Urgent fix to production baseline | main |
| Experimental spike unrelated | main |

---
## 14. Handling Corrections
If a prompt correction occurs (e.g., updating a previously merged response):
- Create new prompt branch with new ID (do **not** reuse old ID) to keep historical chain intact.
- If correction explicitly references an old ID, add tag `correction` in commit message.
- Update chatlog entry per correction protocol.

Rationale: This preserves immutability of earlier merged commit while reflecting the new state.

---
## 15. Audit & Traceability Enhancements (Optional Future)
- `branch_index.md`: Table with columns: Branch | Type | Phase | Status | Last Commit | Prompt ID.
- Append mapping prompt → branch → merge SHA for demo transparency.
- Add CI badge style markers for branch readiness (future automation).

---
## 16. Rollback Procedures
| Case | Action |
|------|--------|
| Unmerged branch abandoned | `git branch -D <branch>` (local) & `git push origin --delete <branch>` |
| Revert merged prompt commit | `git revert <merge_sha>` then update chatlog with corrective prompt |
| Wrong base used | Interactively rebase onto correct base, force push |

---
## 17. Checklist (Per Branch Creation)
- [ ] Determine branch type & base.
- [ ] Generate slug.
- [ ] Create branch.
- [ ] Apply minimal, isolated changes.
- [ ] Stage & verify no secrets.
- [ ] Commit with template fields populated.
- [ ] Open PR & link prompt ID.
- [ ] Merge following strategy.
- [ ] Delete branch if ephemeral.

---
## 18. Assumptions & Defaults Chosen
Some answers were flexible ("if it makes sense"). Defaults applied:
- Always create prompt branches for traceability.
- Long-lived phase branches persist until tagged complete.
- Fast-forward merges preferred for prompt branches; squash allowed for multi-commit feature branches.
- Corrections use **new** prompt ID rather than editing previous commit.
- Branch archive file deferred until ≥5 feature branches merged.

---
## 19. Open Items (Can Revisit Later)
- Implementation of hashing & automation scripts.
- Adoption of branch_index.md aggregator.
- Decision on release branch creation (not required for current scope).

---
## 20. Quick Reference Table
| Action | Command (Example) |
|--------|-------------------|
| Create phase branch | `git checkout -b phase/retrieval` |
| Create prompt branch | `git checkout -b prompt/012-add-chunk-merger phase/retrieval` |
| Commit | `git commit -m "prompt(retrieval): Add chunk merger\n\n[prompt:012] [tags:retrieval,ranking] [hash:HASH_PENDING]\nDetails:\n- Files: backend/app/retrieval.py\n- Rationale: implement merge scoring\n- Response: Response file N/A for reason: stub"` |
| Rebase | `git fetch origin && git rebase origin/main` |
| Fast-forward merge (after PR) | `git checkout main && git merge --ff-only prompt/012-add-chunk-merger` |
| Delete merged branch | `git push origin --delete prompt/012-add-chunk-merger` |

---
**This branching strategy is now the authoritative operational guide.**
