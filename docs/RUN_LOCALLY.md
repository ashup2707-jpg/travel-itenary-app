# Run the app locally

Use this guide to run the app on your machine and verify features (including for a Loom recording).

---

## 1. One-time setup

### 1.1 Create `.env` (project root)

From the **project root** (folder that contains `backend` and `frontend`):

```bash
cp env.template .env
```

Edit `.env` and add your keys. You need **at least one** LLM key for planning:

| Key | Required for | Where to get it |
|-----|--------------|------------------|
| **GROQ_API_KEY** | Planning, edit, explain | https://console.groq.com/ (free tier) |
| **GEMINI_API_KEY** | Same (alternative) | https://makersuite.google.com/app/apikey |
| **SENDER_PASSWORD** | Email “Share” button | Gmail App Password: https://myaccount.google.com/apppasswords |

See [ENV_SETUP.md](ENV_SETUP.md) for full list. At repo root you can also use **PASTE_INTO_DOT_ENV.txt** as a template to copy into `.env`.

### 1.2 Install dependencies

```bash
cd frontend && npm install
cd ../backend && pip3 install -r requirements.txt
```

---

## 2. Start backend and frontend (two terminals)

**Terminal 1 — Backend**

```bash
cd backend
python3 main.py
```

Wait for: `Uvicorn running on http://0.0.0.0:8000` and `Application startup complete`. Keep this terminal open.

**Terminal 2 — Frontend**

```bash
cd frontend
npm run dev
```

Wait for: `Local: http://localhost:3000` and `ready started server`. Keep this terminal open.

**Or use scripts at repo root:** `./start_backend.sh` (terminal 1), `./start_frontend.sh` (terminal 2). Or run `./run_local.sh` to print these commands.

---

## 3. Verify

- **Frontend:** http://localhost:3000  
- **Backend health:** http://localhost:8000/health → `{"status":"healthy"}`  
- **Readiness:** http://localhost:8000/health/ready → `llm_configured`, `email_configured`

In the UI you should see **“● Backend connected”** in the chat header. If you see a message to add an LLM key, add `GROQ_API_KEY` or `GEMINI_API_KEY` to `.env` and restart the backend.

---

## 4. Feature checklist (run each once)

| # | Feature | How to test |
|---|--------|-------------|
| 1 | Planning | “Plan a 3-day trip to Jaipur. I like food and culture, relaxed pace.” → Itinerary with days, blocks, POIs. |
| 2 | RAG / sources | After planning, check Sources panel and POI descriptions. |
| 3 | Edit | “Make Day 2 more relaxed” or “Add a food place to Day 1” → Itinerary updates. |
| 4 | Explain — why | “Why did you pick Hawa Mahal?” → Grounded answer + sources. |
| 5 | Explain — doable | “Is this plan doable?” → Feasibility answer. |
| 6 | Explain — rain | “What if it rains?” → Weather and indoor options. |
| 7 | Share (email) | Click **Share** → Send PDF via Email (optional; clear message if not configured). |

---

## 5. Loom recording script (order of actions)

1. **Intro (~30 s)** — Show Chat | Itinerary | Sources; say “Voice-first AI travel planning assistant.”
2. **Planning (~1–2 min)** — “Plan a 3-day trip to Jaipur. I like food and culture, relaxed pace.” Show itinerary.
3. **RAG (~30 s)** — Point to Sources and POI descriptions; say “Recommendations are grounded in real data.”
4. **Edit (~1 min)** — “Make Day 2 more relaxed”; show only Day 2 changing.
5. **Explanations (~1 min)** — “Why did you pick Hawa Mahal?”, “Is this plan doable?”, “What if it rains?”
6. **Share (~30 s)** — Click Share, show email modal.
7. **Wrap (~15 s)** — “Fully functional locally; next step is deployment.”

---

## 6. Quick reference

| What | URL / command |
|------|----------------|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| Health | http://localhost:8000/health |
| Ready check | http://localhost:8000/health/ready |
| Start backend | `cd backend && python3 main.py` |
| Start frontend | `cd frontend && npm run dev` |
