# API Reference, LLM Usage & Email

Consolidated API endpoints, request/response shapes, LLM usage, and email setup.

---

## 1. Base URL & Health

- **Development:** `http://localhost:8000`
- **Production:** Configure in `.env` (e.g. Render URL)

### `GET /`
API information and list of endpoints (including MCP-backed flows).

### `GET /health`
Health check. Response: `{ "status": "healthy" }`.

### `GET /health/ready`
Demo readiness: `status`, `llm_configured`, `email_configured`, `message`. Use this to verify backend before a Loom recording.

---

## 2. Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/` | API info and list of endpoints |
| `GET` | `/health` | Health check |
| `GET` | `/health/ready` | Readiness (LLM, email) |
| `POST` | `/api/plan` | Create/continue plan from voice/text |
| `POST` | `/api/edit` | Edit itinerary by voice/text command |
| `POST` | `/api/explain` | Ask questions about the plan |
| `GET` | `/api/itinerary` | Get current itinerary + constraints |
| `POST` | `/api/send-email` | Send itinerary as PDF email |
| `POST` | `/api/reset` | Reset planning state |
| `POST` | `/api/eval/feasibility` | Run feasibility eval |
| `POST` | `/api/eval/edit` | Run edit correctness eval |
| `POST` | `/api/eval/grounding` | Run grounding eval |
| `GET` | `/api/eval/all` | Run feasibility + grounding evals |

---

## 3. Planning, Edit, Explain, Email

### `POST /api/plan`
**Body:** `{ "user_input": "Plan a 3-day trip to Jaipur. I like food and culture." }`  
**Response:** `action` (`ask` | `itinerary` | `error`), `itinerary`, `question`, `message`, `rag_loaded`, `rag_citations`, `rag_descriptions`, etc.

### `POST /api/edit`
**Body:** `{ "edit_command": "Make Day 2 more relaxed" }`  
**Response:** `action`, `itinerary`, `changes`, `message`.

### `POST /api/explain`
**Body:** `{ "question": "Why did you pick Hawa Mahal?" }`  
**Response:** `answer`, `citations`, `grounded`.

### `POST /api/send-email`
**Body:** `{ "recipient_emails": ["user@example.com"], "subject": "Your Travel Itinerary from Voyage" }`  
**Response (success):** `{ "success": true, "message": "..." }`.  
**Response (failure):** Backend returns **200** with `success: false`, `message`, and `error` (e.g. `auth`, `connection`, `smtp`) so the frontend can show specific messages.

**Email requirements:** `.env` at **project root** with `SENDER_PASSWORD` (Gmail App Password). Sender/receiver are hardcoded in code; user can override “To” in the Share modal. See [ENV_SETUP.md](ENV_SETUP.md).

---

## 4. Evaluations

- **Feasibility:** `POST /api/eval/feasibility` — current itinerary.
- **Edit correctness:** `POST /api/eval/edit` — body: `original`, `edited`, `edit_request`, `changes`.
- **Grounding:** `POST /api/eval/grounding` — current itinerary + POIs.
- **All:** `GET /api/eval/all` — runs feasibility + grounding.

---

## 5. Error Responses

Endpoints may return `detail` or (for email) a 200 body with `success: false` and `error`.  
Common status codes: `200`, `400`, `500`, `503` (e.g. email not configured).

---

## 6. External & LLM APIs

**LLM:** One `LLMClient` with multiple providers (Groq, Gemini, Grok, OpenAI, Anthropic). Used in: `llm/intent_parser.py`, `llm/constraint_collector.py`, `edit/edit_parser.py`, `rag/explanation_generator.py`. At least one LLM key required for planning/edit/explain.

**Non-LLM:** Nominatim + Overpass (OSM) for POIs; Wikivoyage for RAG; ChromaDB (local) for vector store. See [ARCHITECTURE.md](ARCHITECTURE.md).

---

## 7. CORS & Testing

CORS is enabled for development. For production, set allowed origins in `main.py`.  
Test: `curl http://localhost:8000/health` and `curl -X POST http://localhost:8000/api/plan -H "Content-Type: application/json" -d '{"user_input":"Plan a 2-day trip to Jaipur"}'`.
