# Judging Criteria — Where Each Is Addressed

This document maps the six judging parameters to the codebase so evaluators can see how each is implemented.

---

## 1. Voice UX & Intent Handling — 25%

| Area | Location | What’s implemented |
|------|----------|--------------------|
| **Voice input** | `frontend/pages/index.tsx` | Web Speech API: mic button, `SpeechRecognition`, transcript → input, error handling for unsupported browsers and mic errors. |
| **Intent parsing** | `backend/llm/intent_parser.py` | LLM parses city, duration, interests, pace, dates; structured JSON output; fallback to `SimpleIntentParser` when LLM fails. |
| **Rule-based fallback** | `backend/llm/simple_intent_parser.py` | Regex + keyword extraction for city, duration, interests, pace when LLM unavailable. |
| **Constraint collection** | `backend/llm/constraint_collector.py` | LLM-guided clarification with max 6 questions; symbolic `QuestionCounter`; natural follow-up questions for missing city/duration/interests. |
| **Conversation state** | `backend/orchestration/planning_pipeline.py` | Merges intent with prior constraints; keeps conversation history for multi-turn. |
| **Frontend routing** | `frontend/pages/index.tsx` | Detects plan vs edit vs explain from text (e.g. “make day”, “why”, “doable”, “rain”) and calls `/api/plan`, `/api/edit`, `/api/explain`. |
| **Feedback** | `frontend/pages/index.tsx` | Loading state, error banner, TTS for assistant reply, “Backend connected” / LLM warning in header. |

**Improvements made:** Broader question detection (e.g. “rain”, “weather”), clearer voice/error messages, intent fallback and constraint merge.

---

## 2. MCP Usage & System Design — 20%

| Area | Location | What’s implemented |
|------|----------|--------------------|
| **POI Search MCP** | `backend/mcp_tools/poi_search/` | `POISearchMCP`: takes city, interests, constraints → calls OSM (Nominatim + Overpass); returns ranked POIs with schema `POISearchInput` / `POISearchOutput`. |
| **Itinerary Builder MCP** | `backend/mcp_tools/itinerary_builder/` | `ItineraryBuilderMCP`: takes POIs + time windows + constraints → builds day blocks (morning/afternoon/evening), travel time, feasibility. |
| **Orchestration** | `backend/orchestration/planning_pipeline.py` | Pipeline: intent → constraints → **POISearchMCP.search()** → RAG load → **ItineraryBuilderMCP.build()** → RAG enrichment; edit flow uses POI search for add/swap. |
| **Schemas** | `backend/mcp_tools/poi_search/schema.py`, `itinerary_builder/schema.py` | Pydantic models for inputs/outputs (city, interests, POIs, time windows, constraints). |
| **API surface** | `backend/main.py` | Single entry: `/api/plan` (and edit/explain); MCP tools are internal; root `GET /` lists endpoints and notes MCP-backed flows. |

**Design:** Clear separation: LLM (intent, constraints, explanations), MCP (POI search, itinerary build), RAG (grounding), Symbolic (feasibility, question count).

---

## 3. Grounding & RAG Quality — 15%

| Area | Location | What’s implemented |
|------|----------|--------------------|
| **RAG data** | `backend/rag/jaipur_data.py` | Curated chunks for Jaipur POIs, weather, rainy-day options, indoor activities, plan feasibility; metadata (poi_name, section, source, url). |
| **Vector store** | `backend/rag/vector_store.py` | ChromaDB; cosine similarity; optional `max_distance` filter; dedupe by doc id on load. |
| **RAG loader** | `backend/rag/rag_loader.py` | Loads curated + Wikivoyage; skips duplicate load when data already present; POI name aliases for OSM ↔ RAG match. |
| **Pipeline RAG** | `backend/orchestration/planning_pipeline.py` | POI name aliases; multiple query strategies (descriptive, simple, POI-only, metadata, “tourist attraction”, variations); prefers result with matching `poi_name`; 280-char descriptions; citations with source/section/url. |
| **Explanations** | `backend/rag/explanation_generator.py` | All answers RAG-grounded: “why this place”, “is it doable”, “what if it rains”; LLM optional with RAG-only fallback; citations on every response. |
| **Frontend** | `frontend/pages/index.tsx` | Shows RAG descriptions per POI; Sources panel with citations (source, poi, section). |

**Improvements made:** No duplicate RAG load; POI aliases; extra RAG chunks (weather, rain, indoor, doable); explanation fallbacks; best-match POI for descriptions.

---

## 4. AI Evals & Iteration Depth — 20%

| Area | Location | What’s implemented |
|------|----------|--------------------|
| **Feasibility eval** | `backend/evaluations/feasibility_eval.py` | Daily duration ≤ 12h; travel ≤ 40% of time; POI count vs pace; returns passed, score, checks. |
| **Edit correctness eval** | `backend/evaluations/edit_correctness_eval.py` | Verifies only intended scope changed; compares original vs edited by day/block/POI. |
| **Grounding eval** | `backend/evaluations/grounding_eval.py` | POI grounding (OSM IDs); citation presence; uncertainty handling; returns passed, score, checks. |
| **API** | `backend/main.py` | `POST /api/eval/feasibility`, `POST /api/eval/edit`, `POST /api/eval/grounding`, `GET /api/eval/all` (feasibility + grounding on current state). |
| **Usage** | `backend/evaluations/README.md` | How to run evals (CLI and in code); result shape (passed, score, checks). |
| **Iteration** | Run evals → check scores → adjust prompts (intent, constraint, edit, explanation), RAG chunks, or MCP constraints; re-run evals. |

**Improvements made:** `JUDGING_CRITERIA.md` (this file); `EVALS_ITERATION.md` with run instructions and iteration loop; `/api/eval/all` documented.

---

## 5. Workflow Automation — 10%

| Area | Location | What’s implemented |
|------|----------|--------------------|
| **Planning flow** | `backend/orchestration/planning_pipeline.py` | Single entry `handle_user_input()`: intent → constraints (ask until ready) → POI search → RAG load → itinerary build → RAG enrich; no manual steps. |
| **Edit flow** | `backend/main.py` + `edit_applier.py` | User says edit → `/api/edit` → parse → apply → state updated; POI search MCP used for add/swap. |
| **Explain flow** | `backend/main.py` + `planning_pipeline.explain()` | User asks → `/api/explain` → route by intent (why/doable/rain) → RAG + optional LLM → response. |
| **Local run** | `start_backend.sh`, `start_frontend.sh`, `RUN_LOCALLY.txt`, `LOOM_READY.md` | Scripts and docs for two-terminal run; readiness check `/health/ready`. |

**Improvements made:** Single doc (e.g. LOOM_READY) for “run locally + verify”; optional `run_local.sh` that prints exact commands.

---

## 6. Deployment & Code Quality — 10%

| Area | Location | What’s implemented |
|------|----------|--------------------|
| **Deployment** | `DEPLOYMENT.md`, `RENDER_ENV_SETUP.md`, `render.yaml`, `VERCEL_DEPLOYMENT.md` | Backend (Render), frontend (Vercel), env vars, build/start commands. |
| **API** | `backend/main.py` | FastAPI; CORS; request/response models; HTTP status (400, 503, 500); consistent error messages. |
| **Config** | `env.template`, `PASTE_INTO_DOT_ENV.txt` | Env var list and placeholders; no secrets in repo. |
| **Structure** | `backend/`: llm, mcp_tools, rag, orchestration, edit, symbolic, evaluations; `frontend/`: pages, components | Clear modules; pipeline orchestrates components. |
| **Errors** | `main.py`, `email_sender.py`, frontend | Try/except; user-facing messages (e.g. 503 for email not configured); fallbacks (e.g. RAG-only when LLM fails). |

**Improvements made:** This JUDGING_CRITERIA.md; EVALS_ITERATION.md; README link to LOOM_READY; clear error messages and fallbacks.

---

## Quick Checklist for Evaluators

- **Voice UX (25%):** Use mic or type “Plan a 3-day trip to Jaipur…” → see intent + constraints + itinerary; try edit and explain; check TTS and errors.
- **MCP (20%):** See `mcp_tools/poi_search`, `mcp_tools/itinerary_builder`, and `planning_pipeline.py` for POI search → itinerary build flow.
- **Grounding (15%):** After plan, check Sources and POI descriptions; ask “Why Hawa Mahal?”, “Is it doable?”, “What if it rains?” → answers with citations.
- **Evals (20%):** Create plan, then `GET /api/eval/all` or run `evaluations/` scripts; see feasibility + grounding (and edit if applicable).
- **Workflow (10%):** One flow: plan → edit → explain; scripts/docs for local run.
- **Deployment (10%):** See DEPLOYMENT.md and render.yaml; env from env.template; code structure and error handling as above.
