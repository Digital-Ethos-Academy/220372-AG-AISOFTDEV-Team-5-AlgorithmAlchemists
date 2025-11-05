# Project Context: RAG-Powered Documentation & Query Assistant
Version: 1.0.0

"Unified Context" Mode: All prior standalone agent instruction files have been removed to reduce duplication. The only maintained external procedural documents are:
- `docs/branching_instructions.md` (branching & operational flow)
- `chatlog/chatlog_instructions.md` (chat logging protocol)
All other governance nuances are embedded here. Any historical references to `docs/agent_instructions/` are obsolete.

## 1. Title & Elevator Pitch
**Project Name:** RAG Navigator
**Elevator Pitch:** A developer-focused Retrieval-Augmented Generation (RAG) assistant that ingests plain-text technical documents and answers user queries with sourced, citation-rich responses—demonstrating AI across every SDLC phase in a compressed build window.

## 2. Goals & Success Metrics
**Primary Goal:** Showcase end-to-end AI integration (planning → architecture → code → testing → security → UI) via a working RAG prototype.
**Must-Haves:**
- Functional ingestion of plain text documents.
- Query endpoint returning generated answer + source citations.
- Hybrid retrieval (vector + keyword) for improved relevance.
- Frontend interface (query + citations + dark mode).
- Prompt logging + traceability for SDLC artifacts.
- PlantUML architecture diagrams.
- Dockerized local environment.
**Success Metrics (Demo-Oriented):**
- Query latency: < 2000 ms typical for small corpus.
- Retrieval relevance: qualitatively judged (at least one accurate citing source).
- Backend test coverage target: ~70% core logic (chunking, retrieval, query pipeline).
- UX clarity: straightforward, minimal clicks, dark mode toggle.
- Completeness: All README checklist artifacts delivered.

## 3. Personas
| Persona | Description | Goals |
|---------|-------------|-------|
| Product Owner | Oversees scope & demo viability | See coherent AI-assisted workflow & artifact traceability |
| Developer | Implements backend & retrieval features | Rapid iteration via AI prompts, clean architecture |
| QA Engineer | Validates correctness & resilience | Automated test suite, edge cases covered |
| Technical End-User | Asks questions about ingested docs | Fast, source-backed answers |
| Presenter/Demo Facilitator | Demonstrates system & workflow | Clear narrative: Prompt → Artifact → Result |

## 4. Use Cases
**Core Use Case:** User submits a natural language question; system retrieves relevant chunks from ingested corpus; generates consolidated answer with citations.
**Secondary (Time-Permitting):** Multi-turn chat endpoint reusing retrieval pipeline with conversation history.

## 5. Constraints & Assumptions
- Time budget ≈ 10 hours total (build + prep).
- Local dev environment; no production deployment.
- Plain text documents only for ingestion (short length).
- No authentication (open demo).
- External embedding APIs for simplicity (OpenAI primary). Multi-provider generation possible (OpenAI / Anthropic / Gemini).
- Real API keys available via `.env` (not committed).
- Corpus size small (≈5–7 synthetic documents).

## 6. High-Level Architecture Overview
**Components:**
- Frontend (React + Tailwind) – Query UI, dark mode toggle, model selection.
- Backend (FastAPI) – Ingestion, retrieval, generation, logging.
- RAG Pipeline – Chunking → Embedding → Hybrid Retrieval (vector + keyword) → Context Assembly → Generation.
- Storage (SQLite) – Documents, Chunks (+ embeddings metadata), QueryLog.
- Vector Index – In-memory (FAISS or Python-side matrix); cached at startup.
**Diagrams (PlantUML Planned):** System Context, Component Diagram, Query Sequence Flow.

## 7. Data Model
**Tables (SQLite):**
- `documents`: id (PK), filename, text, created_at.
- `chunks`: id (PK), document_id (FK), content, embedding (BLOB or JSON), position, created_at.
- `query_log`: id (PK), query, model_used, top_k, latency_ms, created_at.
(Optional separate `embeddings` table omitted for simplicity; embedding stored inline with chunk.)
**Indexes:**
- Full-text or LIKE search (keyword fallback) on `chunks.content`.
- Document-chunk foreign key.

## 8. Retrieval & Generation Flow
1. User calls `/query` with `{"query": "..."}`.
2. Normalize query (trim, lower-case for keyword pass).
3. Embed query via external embedding provider.
4. Vector similarity: compute distances vs stored chunk embeddings (top_k vector set).
5. Keyword match: simple scoring (term frequency / presence) to collect candidate set.
6. Merge & rank hybrid results (vector score + keyword bonus heuristic).
7. Assemble context (top_k=5 default) – join chunk contents with source markers.
8. Call selected generative model (OpenAI default) with system + retrieval prompt.
9. Return answer + structured sources + latency.

## 9. API Endpoints (Initial Contract)
| Endpoint | Method | Description | Request | Response |
|----------|--------|-------------|---------|----------|
| `/ingest` | POST | Upload plain text to create document & chunks | `{"filename": "x.txt", "text": "..."}` | `{"document_id": 1, "chunks_created": 12}` |
| `/documents` | GET | List documents (pagination optional) | `?page=&size=` | `{"documents": [...], "total": n}` |
| `/query` | POST | Single-turn RAG answer | `{"query": "...", "model": "openai"?}` | Approved shape below |
| `/chat` | POST | Multi-turn (optional) | `{"messages": [...], "model": "..."}` | Chat variation of query response |
| `/health` | GET | Health check | none | `{"status": "ok"}` |

**/query Response Shape (Approved):**
```json
{
  "query": "original question",
  "answer": "generated answer text",
  "sources": [
    {"doc_id": 1, "filename": "doc1.txt", "score": 0.87, "excerpt": "matching text snippet"}
  ],
  "latency_ms": 542
}
```
**Error Format:** `{ "detail": "error message" }`.

## 10. Frontend Plan
**Framework:** React (Hooks) + Tailwind CSS + Dark Mode Toggle.
**Layout:** Sidebar (query input history, ingestion trigger) + Main Panel (answer + sources). Model selection dropdown.
**Components:**
- `SidebarQueryHistory`
- `ChatUI` (or `QueryPanel` for single-turn)
- `DocumentUploader` (POST /ingest)
- `QueryResult` (answer + expandable citations)
- `DarkModeToggle`
**UX Priorities:** Speed, clarity, minimal friction, accessible dark/light contrast.

## 11. Prompt Logging & Traceability
**Format:** Dual-write JSON + Markdown per prompt.
**Fields:** id, timestamp, phase, intent, prompt, context_files, model, params, response_excerpt, artifacts_created, decisions, next_actions, tags.
**Versioning Rule:** Increment version when prompt text changes >20% or output materially shifts artifact direction.
**Markdown Diff:** Include previous prompt excerpt + major changes on versioned updates.
**Storage:** `prompts/index.json` + `prompts/YYYY-MM-DD/prompt-XXX.{json,md}`.

## 12. Architecture Decision Records (ADRs)
**Purpose:** Capture key technical decisions & trade-offs.
**Template Fields:** Title, Context, Decision, Status, Consequences.
**Planned ADRs:**
1. RAG Hybrid Retrieval Strategy (vector + keyword).
2. External Embeddings vs Local Model.
3. Dual-Format Prompt Logging.
4. Local Docker Compose Deployment.
5. Inlined Embeddings in Chunk Table.

## 13. Testing Strategy
**Unit Tests:** Chunking procedure, vector ranking merger, keyword fallback scoring.
**Integration Tests:** /ingest creates document & chunks; /query returns answer with ≥1 source.
**Negative Tests:** Empty query, excessively long query (truncate or reject), injection attempt phrase inside corpus.
**Security Edge Checks:** Encoded HTML script tags ingested—ensure harmless usage.
**Coverage Goal:** ~70% for core modules; prioritize retrieval pipeline correctness.

## 14. Security & Threat Model (Descriptive Only)
**Assets:** API keys, document corpus, user query history.
**Threats:** Prompt injection (malicious text altering generation), malicious ingestion (oversized payload), data leakage (exposing entire corpus inadvertently).
**Mitigations (Described):**
- Enforce max text size on ingestion.
- Basic sanitization: strip HTML tags.
- Limit context size per query.
- Log queries for audit.

## 15. Performance & Observability
- Measure total latency per /query (ms).
- Log retrieval scores + chosen chunks (debug mode optional).
- In-memory vector index (rebuilt at ingestion or startup seed).
- Potential simple caching: last N embeddings (if same query repeated).

## 16. Seeding Strategy
**Synthetic Documents (5–7):** Topics: SDLC Phases, FastAPI Basics, React Patterns, Prompt Engineering Principles, RAG Overview, Testing Strategies.
**Seed Script:** `scripts/seed.py` checks if documents exist; if not, loads synthetic texts and calls /ingest for each.
**Startup:** Backend entrypoint optionally invokes seed prior to serving.

## 17. Environment Variables
```
TAVILY_API_KEY=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=
HUGGINGFACE_API_KEY=
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-3-small
TOP_K_DEFAULT=5
CHUNK_SIZE=800
CHUNK_OVERLAP=100
```
**Notes:** `.env.example` included; real `.env` excluded from VCS.

## 18. Docker & Dev Workflow
**docker-compose.yml:**
- Service `backend`: FastAPI app, runs seed then uvicorn.
- Service `frontend`: React dev server.
**Ports:** Backend 8000, Frontend 3000 (default).
**Volumes:** Optional for live reload of backend code.
**Simplified Dockerfiles:** Avoid multi-stage unless required for image size.

## 19. Timeline & Roadmap (Condensed)
1. Scaffold repo & context docs.
2. Data model + chunking + ingestion endpoint.
3. Embedding + vector index + hybrid retrieval.
4. Query endpoint + answer formatting.
5. Frontend components + dark mode + model selection.
6. Testing suite + security review markdown.
7. PlantUML diagrams + ADRs.
8. Prompt logs compilation + polish.

## 20. Presentation Outline
1. Title & Problem Statement.
2. Personas & Use Cases.
3. AI-Assisted Workflow (Prompt → Artifact examples).
4. Architecture (Diagrams + RAG Flow).
5. Live Demo (Ingest → Query → Citation).
6. Testing & Security Summary.
7. Metrics & Reflections.
8. Future Enhancements.

## 21. Future Enhancements (Out of Scope)
- Re-ranking layer integration.
- Multi-turn memory persistence across sessions.
- Role-based access & auth.
- Advanced analytics dashboard.
- Incremental indexing / real-time updates.

## 22. Glossary
| Term | Definition |
|------|------------|
| RAG | Retrieval-Augmented Generation: combine retrieved context with generative model output. |
| Chunk | Subdivision of a document for fine-grained retrieval. |
| Embedding | Numeric vector representation of text meaning. |
| Hybrid Retrieval | Combines vector similarity with keyword matching. |
| Citation | Source snippet + metadata returned with answer. |
| ADR | Architecture Decision Record documenting a key decision & trade-offs. |
| Prompt Log | Recorded input prompt + metadata + response excerpt for traceability. |

## 23. Open Decisions / TBD
- Final decision to include /chat endpoint (time-based).
- Whether to persist conversation state (likely skipped).
- Potential fallback embedding provider if OpenAI unavailable.

## 24. Acceptance Criteria Summary
- Run docker-compose: both services start successfully.
- Seed documents appear in `/documents` list.
- `/query` returns answer with ≥1 citation, latency_ms field populated.
- Dark mode toggle changes theme correctly.
- Prompt logs exist (`prompts/index.json` + markdown entries) with versioning.
- PlantUML diagrams present in `docs/` (system context, component, sequence).
- ADR files (≥3) present and populated.
- Test suite runs and passes (core pipeline tests included).

## 25. File/Directory Plan (Planned)
```
backend/
  app/
    main.py
    models.py
    retrieval.py
    ingestion.py
    schemas.py
    config.py
  tests/
    test_ingest.py
    test_query.py
    test_retrieval.py
frontend/
  src/
    components/
      ChatUI.jsx
      QueryResult.jsx
      SidebarQueryHistory.jsx
      DocumentUploader.jsx
      DarkModeToggle.jsx
    App.jsx
    index.jsx
  tailwind.config.js
  package.json
scripts/
  seed.py
  log_prompt.py
prompts/
  index.json
  2025-11-05/
    prompt-001.md
    prompt-001.json
docs/
  PROJECT_CONTEXT.md
  architecture.md
  prd.md
  security_review.md
  adr/
    ADR-001-hybrid-retrieval.md
    ADR-002-external-embeddings.md
    ADR-003-prompt-logging.md
.env.example
docker-compose.yml
README.md
```

## 26. Implementation Notes & Rationale Highlights
- Hybrid retrieval improves relevance with minimal complexity.
- Inlining embeddings reduces joins and schema footprint.
- External embeddings offload model hosting complexity.
- Prompt logging enables presentation transparency.
- Synthetic seed ensures deterministic demo behavior.

## 27. Next Immediate Steps
1. Scaffold directories & placeholder files.
2. Implement ingestion + chunking.
3. Build embedding + vector index utilities.
4. Implement retrieval merge + /query endpoint.
5. Wire frontend basic query flow.
6. Add tests + logging + diagrams.

---
**This document is the authoritative context reference for subsequent AI-assisted generation and implementation.**

---
## Operational Chat Logging Directive (Embedded)

Use the logging protocol in `chatlog/chatlog_instructions.md` verbatim. Core rules (embedded for convenience; canonical source remains that file to allow focused maintenance):
1. After each assistant reply: prepend a new row to `chatlog/index.md`, create the full response markdown file, and append an entry to `chatlog/transcript.md`.
2. IDs: sequential integers starting at 1; never renumber; corrections reuse ID.
3. Timestamps: ISO 8601 UTC (`YYYY-MM-DDThh:mm:ssZ`). Filename replaces `:` with `-`.
4. Summary: single sentence (≤200 chars) abstract of response intent; ends with a period.
5. Tags: 1–5 lowercase keywords auto-inferred; add `correction` when overwriting.
6. Hash field remains `HASH_PENDING` until hashing routine adopted.
7. Corrections: overwrite full response file + update existing index row (add `correction` tag); append transcript note. Do not create a new ID for a correction.
8. Atomicity: All three surfaces must update in one action; if partial failure, remediate before next turn.

For full template specifics, validation regex, and edge-case handling consult `chatlog/chatlog_instructions.md`. That file is the definitive procedural reference; this section is a convenience snapshot.

