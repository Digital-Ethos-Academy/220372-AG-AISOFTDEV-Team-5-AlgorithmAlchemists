---
description: "Answer canonical project fact questions with exact fact text and confidence, or escalate if low confidence"
mode: "ask"
---
Given a user question, attempt to match it to canonical facts.

Required Output JSON:
{
  "question": <string>,
  "answer": <string>,
  "confidence": <float>,
  "source_fact_id": <string>,
  "escalation": <null|"Consult Mentor">,
  "explanation": <string concise>
}

Algorithm Guidance (non-executable):
1. Tokenize question; compute overlap with fact tokens.
2. confidence = overlap_tokens / question_tokens (cap 1.0).
3. If confidence < 0.85 return escalation = "Consult Mentor" and do NOT fabricate answer.
4. For multi-fact tie choose fact with most recent `last_updated` surrogate.

Safety:
- If no fact matches, return {"error":"no_match"}.
- Do not generate speculative content; answer must be exact or concise paraphrase preserving meaning.
