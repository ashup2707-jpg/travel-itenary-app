# Start Here — For Evaluators

This app is a **voice-first AI travel planning assistant**: users speak or type to plan trips, edit itineraries, and ask grounded questions (“Why this place?”, “Is it doable?”, “What if it rains?”). The backend uses LLM + MCP (POI Search, Itinerary Builder) + RAG for grounding.

---

## How to navigate the repo

| Step | What to read | Purpose |
|------|----------------|--------|
| 1 | **[../README.md](../README.md)** | Project overview, quick start, doc index |
| 2 | **[ARCHITECTURE.md](ARCHITECTURE.md)** | High-level flow (intent → constraints → MCP → RAG), folder layout |
| 3 | **[JUDGING_CRITERIA.md](JUDGING_CRITERIA.md)** | Where each judging parameter (Voice UX, MCP, Grounding, Evals, Workflow, Deployment) is implemented |
| 4 | **[RUN_LOCALLY.md](RUN_LOCALLY.md)** | How to run backend + frontend locally and verify features |
| 5 | **[API_AND_ENDPOINTS.md](API_AND_ENDPOINTS.md)** | API reference, LLM usage, email setup |
| 6 | **[EVALS_ITERATION.md](EVALS_ITERATION.md)** | How to run evals (API + code) and iterate |
| 7 | **[DEPLOYMENT.md](DEPLOYMENT.md)** | Deploy backend (Render) and frontend (Vercel) |

---

## Quick links by judging criterion

| Criterion | Where to look |
|----------|----------------|
| **Voice UX & intent (25%)** | JUDGING_CRITERIA.md §1; `backend/llm/intent_parser.py`, `constraint_collector.py`; `frontend/pages/index.tsx` (voice, routing) |
| **MCP & system design (20%)** | JUDGING_CRITERIA.md §2; `backend/mcp_tools/poi_search/`, `mcp_tools/itinerary_builder/`; `backend/orchestration/planning_pipeline.py` |
| **Grounding & RAG (15%)** | JUDGING_CRITERIA.md §3; `backend/rag/` (jaipur_data, vector_store, explanation_generator); pipeline RAG logic |
| **AI evals & iteration (20%)** | JUDGING_CRITERIA.md §4; EVALS_ITERATION.md; `backend/evaluations/`; `GET /api/eval/all` |
| **Workflow automation (10%)** | JUDGING_CRITERIA.md §5; RUN_LOCALLY.md; `start_backend.sh`, `start_frontend.sh`, `run_local.sh` |
| **Deployment & code quality (10%)** | JUDGING_CRITERIA.md §6; DEPLOYMENT.md; `backend/main.py`; `env.template` |

---

## Run the app in 3 steps

1. **Env:** Copy `env.template` to `.env` in the **project root** and add `GROQ_API_KEY` (or another LLM key). See [ENV_SETUP.md](ENV_SETUP.md) or `PASTE_INTO_DOT_ENV.txt` at repo root.
2. **Backend:** In a terminal: `cd backend && python3 main.py` (leave running).
3. **Frontend:** In another terminal: `cd frontend && npm install && npm run dev`, then open **http://localhost:3000**.

Details: [RUN_LOCALLY.md](RUN_LOCALLY.md).

---

## Doc index (all docs in this folder)

| File | Contents |
|------|----------|
| **00_EVALUATOR_START_HERE.md** | This file — navigation for evaluators |
| **ARCHITECTURE.md** | Flow diagram, tech stack, folder structure |
| **JUDGING_CRITERIA.md** | Mapping of all 6 criteria to code |
| **RUN_LOCALLY.md** | Local run, verification, Loom checklist |
| **API_AND_ENDPOINTS.md** | Endpoints, request/response, LLM & email |
| **EVALS_ITERATION.md** | Run evals, interpret scores, iterate |
| **ENV_SETUP.md** | .env variables and where to get keys |
| **DEPLOYMENT.md** | Render + Vercel deployment overview |
| **RENDER_ENV_SETUP.md** | Render-specific env and build |
| **VERCEL_DEPLOYMENT.md** | Vercel frontend deploy + troubleshooting |
