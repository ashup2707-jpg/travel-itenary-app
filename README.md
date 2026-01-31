# Voice-First AI Travel Planning Assistant

A capstone-grade voice-first travel planning assistant that reasons about feasibility, supports incremental edits, and provides grounded explanations.

## ✅ Project Status: Complete

All required components implemented and working.

## Architecture

**Hybrid LLM + Symbolic Architecture**
- **LLM Layer:** Natural language understanding, intent parsing, explanations
- **Symbolic Layer:** Feasibility analysis, constraint validation, edit scoping
- **MCP Tools:** POI Search, Itinerary Builder
- **RAG System:** Wikivoyage/Wikipedia for grounded explanations

## Tech Stack

- **Backend:** Python 3.9+ (FastAPI)
- **Frontend:** React/Next.js (TypeScript)
- **LLM:** Multi-provider support with automatic fallback
  - Grok by xAI (grok-beta) - **First Priority** ⭐
  - Groq (llama-3.1-70b) - **Ultra-fast, 14,400 free/day!** 🚀
  - OpenAI GPT (gpt-3.5-turbo, gpt-4)
  - Google Gemini (gemini-1.5-flash)
  - Anthropic Claude (claude-3-sonnet)
- **Vector DB:** Chroma (local, free)
- **Voice:** Web Speech API (browser-based, free)
- **Email:** SMTP (Gmail, Outlook, etc.)

## Documentation (evaluators start here)

**→ [docs/00_EVALUATOR_START_HERE.md](docs/00_EVALUATOR_START_HERE.md)** — Navigation for evaluators and quick links by criterion.  
**→ Where each judging parameter is implemented: [docs/JUDGING_CRITERIA.md](docs/JUDGING_CRITERIA.md)**  
**→ How to run evals and iterate: [docs/EVALS_ITERATION.md](docs/EVALS_ITERATION.md)**  
**→ Local run and Loom checklist: [docs/RUN_LOCALLY.md](docs/RUN_LOCALLY.md)**  
**→ All docs:** [docs/](docs/) (ARCHITECTURE, API_AND_ENDPOINTS, ENV_SETUP, DEPLOYMENT, VERCEL_DEPLOYMENT, RENDER_ENV_SETUP).

## Quick Start

### 1. Backend Setup

```bash
cd backend
pip3 install -r requirements.txt
```

### 2. Create .env File

Create a `.env` file in the **project root** (parent of `backend` and `frontend`). See **[docs/ENV_SETUP.md](docs/ENV_SETUP.md)** for full variables and where to get keys. Minimal example:

```bash
# =============================================================================
# LLM API Keys (Add at least one - system uses automatic fallback)
# Priority: Grok → Groq → OpenAI → Gemini → Anthropic
# =============================================================================

# 🔥 Grok by xAI - FIRST PRIORITY (https://console.x.ai/)
GROK_API_KEY=your_grok_api_key_here
GROK_MODEL=grok-beta

# 🚀 Groq - ULTRA-FAST & FREE (https://console.groq.com/)
# 14,400 requests/day FREE! Get this one!
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-70b-versatile

# OpenAI (https://platform.openai.com/api-keys)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Google Gemini (https://makersuite.google.com/app/apikey)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash

# Anthropic Claude (https://console.anthropic.com/)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# =============================================================================
# Email Configuration (Required - for sending itineraries as PDF)
# =============================================================================

# Email addresses are hardcoded:
# - Sender: ashup2707@gmail.com
# - Receiver: f20201480g@alumni.bits-pilani.ac.in

# For Gmail App Password:
# 1. Go to: https://myaccount.google.com/apppasswords
# 2. Sign in with ashup2707@gmail.com
# 3. Select "Mail" and "Other (Custom name)" → Enter "Travel Planner"
# 4. Click "Generate"
# 5. Copy the 16-character App Password (format: xxxx xxxx xxxx xxxx)
# 6. Paste it below (remove spaces)

SENDER_PASSWORD=your_16_character_gmail_app_password_here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# =============================================================================
# Backend Configuration
# =============================================================================

BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000
TARGET_CITY=Jaipur
```

**Important Notes:**
- **LLM Keys:** You need at least ONE LLM API key. The system automatically falls back to other providers if rate limits are hit.
- **Priority Order:** Grok → Groq → OpenAI → Gemini → Anthropic (uses whichever keys are available)
- **Recommended:** Get **Groq** (14,400 free requests/day!) - See `FREE_API_GUIDE.md`
- **Email:** Optional - app works without it, but you won't be able to send itineraries via email
- **Gmail Setup:** Must use App Password (not your regular password) if using 2FA

### 3. Run Backend

```bash
python3 main.py
```

### 4. Frontend Setup (new terminal)

```bash
cd frontend
npm install
npm run dev
```

### 5. Open in Browser

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Project Structure

```
.
├── backend/
│   ├── data_sources/     # OSM, Wikivoyage clients
│   ├── edit/             # Edit parser and applier
│   ├── evaluations/      # 3 evaluation systems
│   ├── llm/              # LLM client, intent parser
│   ├── mcp_tools/        # POI Search, Itinerary Builder
│   ├── orchestration/    # Planning pipeline
│   ├── rag/              # Vector store, explanations
│   ├── symbolic/         # Feasibility engine
│   └── main.py           # FastAPI app
├── frontend/
│   ├── components/       # Voice UI components
│   └── pages/            # Main page
└── test_transcripts/     # Sample conversations
```

## MCP Tools

### 1. POI Search MCP
- **Input:** city, interests, constraints
- **Output:** ranked POIs with OSM IDs
- **Location:** `backend/mcp_tools/poi_search/`

### 2. Itinerary Builder MCP
- **Input:** candidate POIs, time windows, pace
- **Output:** structured day-wise itinerary
- **Location:** `backend/mcp_tools/itinerary_builder/`

## Datasets

- **OpenStreetMap (Overpass API)** - Points of Interest
- **Wikivoyage** - City guides and travel tips
- **Wikipedia** - Detailed POI information

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/plan` | POST | Create/continue planning |
| `/api/edit` | POST | Edit itinerary |
| `/api/explain` | POST | Answer questions |
| `/api/send-email` | POST | Send itinerary via email |
| `/api/itinerary` | GET | Get current itinerary |
| `/api/eval/feasibility` | POST | Run feasibility eval |
| `/api/eval/grounding` | POST | Run grounding eval |
| `/api/eval/all` | GET | Run all evaluations |
| `/api/reset` | POST | Reset session |

## Evaluations

### 1. Feasibility Evaluation
- Daily duration ≤ available time
- Reasonable travel times
- Pace consistency

### 2. Edit Correctness Evaluation
- Voice edits only modify intended sections
- No unintended changes elsewhere

### 3. Grounding & Hallucination Evaluation
- POIs map to OSM records
- Tips cite RAG sources
- Uncertainty explicitly stated

### Run Evaluations

```bash
cd backend
python3 evaluations/feasibility_eval.py
python3 evaluations/edit_correctness_eval.py
python3 evaluations/grounding_eval.py
```

## Sample Test Transcripts

See `test_transcripts/` folder:
- `sample_planning.txt` - Planning session
- `sample_edit.txt` - Edit session
- `sample_explanation.txt` - Explanation session

## Features

### 🎤 Voice-First Interface
- **Speech-to-Text:** Browser's native Web Speech API (free, no API calls)
- **Text-to-Speech:** Browser's native SpeechSynthesis API (free, no API calls)
- Works in Chrome, Edge, and other modern browsers

### 🤖 Multi-LLM Support with Automatic Fallback
- Supports **5 providers:** Grok (xAI), Groq, OpenAI, Gemini, Anthropic
- **Priority:** Grok first, then Groq (14,400 free/day!)
- **Automatic fallback** on rate limits or errors
- No downtime - seamlessly switches providers
- Use multiple providers to stay within free tiers
- **See `FREE_API_GUIDE.md` for setup** 🚀

### 📧 Email Itineraries
- Send completed itineraries to up to 2 email addresses
- Beautiful HTML-formatted emails
- Click "📧 Send Email" button when itinerary is ready

### 🗣️ Voice Commands

#### Planning
- "Plan a 3-day trip to Jaipur. I like food and culture, relaxed pace."

#### Editing
- "Make Day 2 more relaxed"
- "Swap the Day 1 evening plan to something indoors"
- "Add one famous local food place"
- "Reduce travel time"

#### Explanations
- "Why did you pick this place?"
- "Is this plan doable?"
- "What if it rains?"

## License

Capstone Project - Educational Use
