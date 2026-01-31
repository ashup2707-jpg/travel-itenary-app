# Architecture

## What the app does

Users speak or type to **plan** a trip (e.g. “3-day trip to Jaipur, food and culture”), **edit** the itinerary (“Make Day 2 more relaxed”), and **ask** grounded questions (“Why this place?”, “Is it doable?”, “What if it rains?”). The backend parses intent, collects constraints, searches POIs (MCP), builds the itinerary (MCP), enriches with RAG, and answers questions using RAG + optional LLM.

---

## High-level flow

```
User input (voice/text)
    → Intent parsing (LLM or rule-based)
    → Constraint collection (LLM + symbolic, max 6 questions)
    → POI Search MCP (OpenStreetMap)
    → RAG load (curated + Wikivoyage)
    → Itinerary Builder MCP (time blocks, feasibility)
    → RAG enrichment (descriptions, citations)
    → Response (itinerary + sources)
```

**Edit flow:** User says edit → Edit parser (LLM) → Edit applier (symbolic + POI Search MCP for add/swap) → Updated itinerary.

**Explain flow:** User asks question → Route (why / doable / rain) → RAG + optional LLM → Grounded answer + citations.

---

## Tech stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.9+, FastAPI |
| Frontend | React, Next.js, TypeScript |
| LLM | Groq, Gemini (and optional OpenAI, Anthropic, Grok) with fallback |
| Voice | Web Speech API (browser) |
| MCP | POI Search (OSM), Itinerary Builder (in-process) |
| RAG | ChromaDB, curated Jaipur data + Wikivoyage |
| Email | SMTP (Gmail) |

---

## Folder structure

```
project root/
├── README.md                 # Main entry, doc index
├── env.template              # Env var template
├── PASTE_INTO_DOT_ENV.txt    # Copy into .env (see docs/ENV_SETUP.md)
├── start_backend.sh          # Start backend
├── start_frontend.sh         # Start frontend
├── run_local.sh              # Print run commands
├── docs/                     # All documentation (start with 00_EVALUATOR_START_HERE.md)
├── backend/
│   ├── main.py               # FastAPI app, routes
│   ├── email_sender.py       # SMTP, PDF itinerary
│   ├── data_sources/         # OSM client, Wikivoyage scraper
│   ├── llm/                  # Intent parser, constraint collector, LLM client
│   ├── mcp_tools/            # POI Search MCP, Itinerary Builder MCP
│   ├── orchestration/        # Planning pipeline (orchestrates all)
│   ├── rag/                  # Vector store, RAG loader, explanation generator, jaipur_data
│   ├── edit/                 # Edit parser, edit applier
│   ├── symbolic/             # Feasibility engine, question counter
│   └── evaluations/          # Feasibility, edit correctness, grounding evals
├── frontend/
│   ├── pages/index.tsx       # Main UI (chat, itinerary, sources, share)
│   └── components/          # Voice UI components
└── test_transcripts/        # Sample planning/edit/explanation transcripts
```

---

## Where key behavior lives

| Feature | Primary location |
|--------|-------------------|
| Voice UX, intent routing | `frontend/pages/index.tsx`; `backend/llm/intent_parser.py`, `constraint_collector.py` |
| MCP: POI search | `backend/mcp_tools/poi_search/` |
| MCP: Itinerary build | `backend/mcp_tools/itinerary_builder/` |
| Pipeline (plan flow) | `backend/orchestration/planning_pipeline.py` |
| RAG data & queries | `backend/rag/jaipur_data.py`, `rag_loader.py`, `vector_store.py`; pipeline RAG logic |
| Grounded explanations | `backend/rag/explanation_generator.py`; pipeline `explain()` |
| Evals | `backend/evaluations/`; `GET /api/eval/all` |

For the full mapping of judging criteria to code, see [JUDGING_CRITERIA.md](JUDGING_CRITERIA.md).
