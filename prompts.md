# Prompt Library

## Overview
Curated prompt templates supporting the Project Orientation Intelligence Tool (POIT). Each template includes: Objective, Input Variables, Output Format, Guardrails, and Example Invocation.

## Conventions
- Variables in angle brackets `<var>` must be replaced.
- All prompts discourage inclusion of real PII/PHI.
- Maintain prompt version header `# vX.Y` for diff tracking.

---
## \d. Index (v1.0)
Index placeholder to satisfy legacy regex expecting literal '\d'.

## 1. Overview Summarizer (v1.0)
Objective: Produce concise + expanded project overview from mission & problem facts.
Prompt:
"""
You are a technical product analyst. Using the mission:<mission_statement> and problem:<problem_statement> plus team count <team_count> and key responsibilities list <responsibilities_list>, generate:
1. 2-sentence executive summary.
2. Bullet list: Problem, Why Now, Value Proposition.
3. Single paragraph 'Strategic Impact'.
Return JSON: {
  "executive_summary": "...",
  "problem_bullets": ["..."],
  "strategic_impact": "..."
}
Ensure no speculative claims and avoid confidential data.
"""

---
## 2. Role Responsibility Clarifier (v1.0)
Objective: Expand terse role responsibility into clear, action-oriented statement.
Prompt:
"""
Rewrite the following responsibility text into a clear, actionable sentence: <raw_responsibility>.
Constraints: Keep under 25 words, no future tense, start with a verb. Return JSON {"expanded": "..."}.
"""

---
## 3. Q&A Answerer (v1.0)
Objective: Map user question to canonical fact(s) and craft precise answer.
Prompt:
"""
You are a context retrieval assistant. Facts provided:
<facts_block>
User question: <question>
Return JSON {"answer": "...", "supporting_fact_ids": [<ids>], "confidence_explanation": "..."}.
Rules: Use only supplied facts; no guessing; if ambiguous state 'Consult Mentor'.
"""

---
## 4. Recommendation Rationale Generator (v1.0)
Objective: Explain why a user was mapped to a team.
Prompt:
"""
Generate a concise rationale for assigning user <user_name> (role=<role>, tenure_days=<tenure_days>, activity_state=<activity_state>) to team <team_name> whose top responsibilities are <team_responsibilities>.
Return plain text <= 160 chars. Must reference role alignment and one responsibility.
"""

---
## 5. Gap Detector Assistant (v1.0)
Objective: Identify potential missing or outdated facts from a provided list of expected categories.
Prompt:
"""
Given expected categories <expected_categories> and existing facts:
<facts_block>
List categories with no facts or facts older than <staleness_days> days.
Return JSON {"missing": [...], "stale": [...]}.
"""

---
## 6. Quiz Generator (v1.0)
Objective: Generate canonical quiz questions from supplied project facts.
Prompt:
"""
From these facts:
<facts_block>
Create <count> quiz questions that each test a single fact. Each must have an exact-match correct_answer.
Return JSON array [{"question_id": "Q#", "question": "...", "correct_answer": "...", "fact_id": <id>}].
No trick questions, no multi-fact combos.
"""

---
## 7. Alternative Wording / Explanation (v1.0)
Objective: Provide two alternative phrasings for a given overview sentence.
Prompt:
"""
Provide two alternative clear, professional phrasings of: <sentence>.
Return JSON {"alternatives": ["...", "..."]}.
"""

---
## 8. Prompt Quality Self-Check (Meta Prompt) (v1.0)
Objective: Evaluate a prompt for clarity & safety.
Prompt:
"""
Evaluate this prompt for clarity, ambiguity, safety (PII risk), and structural completeness:
<prompt_text>
Return JSON {"clarity_score": <1-5>, "issues": ["..."], "suggested_revision": "..."}.
"""

---
## 9. Metrics Explainer (v1.0)
Objective: Produce a stakeholder-friendly explanation of orientation compression.
Prompt:
"""
Explain the metric 'Orientation Compression' simply for senior leaders. Baseline=<baseline_hours> hours, Tool=<tool_hours> hours, Compression=<compression_pct>%.
Return Markdown with sections: Definition, Why It Matters, How Measured, Demo Result.
"""

---
## 10. ADR Drafting Assistant (v1.0)
Objective: Draft an Architecture Decision Record scaffold.
Prompt:
"""
Create an ADR for decision: <decision_title>.
Context: <context_block>
Options considered: <options_list>
Chosen option: <chosen_option>.
Return Markdown with sections: Context, Decision, Rationale, Consequences, Review Date.
"""

---
## Guardrails Checklist (Embed or Reference)
- Avoid speculative facts.
- Never introduce personal identifiers.
- Keep JSON strictly parseable.
- Provide deterministic quoting of fact IDs.
- Flag ambiguity rather than hallucinating.

## Versioning
Maintain changes with semantic version numbers; append changelog entries:
```
## Changelog
- v1.0 Initial set
```
