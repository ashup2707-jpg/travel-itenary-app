# Deployment Guide

## Quick Deploy Options

### Backend Deployment

#### Option 1: Railway (Recommended - Free tier)
1. Create account at https://railway.app
2. New Project → Deploy from GitHub
3. Add environment variables:
   ```
   GEMINI_API_KEY=your_key
   BACKEND_PORT=8000
   ```
4. Deploy! Get public URL

#### Option 2: Render (Free tier)
1. Create account at https://render.com
2. New Web Service → Connect GitHub
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `cd backend && python main.py`
5. Add environment variables
6. Deploy!

#### Option 3: Vercel (Serverless)
1. Create account at https://vercel.com
2. New Project → Import from Git
3. Framework: Other
4. Build settings: None
5. Add env vars
6. Deploy!

### Frontend Deployment (If Node.js installed)

#### Vercel (Recommended)
```bash
cd frontend
npm install
npm run build
vercel deploy
```

#### Netlify
```bash
cd frontend
npm install
npm run build
netlify deploy
```

---

## Demo Video Script (5 minutes)

### Part 1: Introduction (30 sec)
- Show architecture diagram
- Explain Hybrid LLM + Symbolic approach
- Mention 2 MCP tools + RAG

### Part 2: Voice Planning (1.5 min)
- Make API call showing trip request
- Show generated 3-day itinerary
- Highlight day-wise blocks with POIs

### Part 3: Voice Editing (1 min)
- Show edit command: "Make Day 2 more relaxed"
- Show only Day 2 changed
- Explain edit scoping

### Part 4: Explanation & RAG (1 min)
- Ask "Why Hawa Mahal?"
- Show citations from Wikipedia, TripAdvisor
- Show sources in response

### Part 5: Evaluations (1 min)
- Run feasibility eval (show 90% score)
- Run grounding eval (show citations)
- Explain what's being validated

### Part 6: Wrap-up (30 sec)
- Show MCP tools used
- Show datasets (OSM, Wikivoyage)
- Show GitHub repo

---

## Environment Variables Needed

```env
GEMINI_API_KEY=your_gemini_api_key
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000
TARGET_CITY=Jaipur
```

---

## Public Demo Commands

Once deployed, share these curl commands for demo:

### 1. Create Plan
```bash
curl -X POST https://your-backend-url.com/api/plan \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Plan a 3-day trip to Jaipur. I like food and culture, relaxed pace."}'
```

### 2. Explain
```bash
curl -X POST https://your-backend-url.com/api/explain \
  -H "Content-Type: application/json" \
  -d '{"question": "Why did you pick Hawa Mahal?"}'
```

### 3. Edit
```bash
curl -X POST https://your-backend-url.com/api/edit \
  -H "Content-Type: application/json" \
  -d '{"edit_command": "Make Day 2 more relaxed"}'
```

### 4. Evaluate
```bash
curl https://your-backend-url.com/api/eval/all
```

---

## Submission Checklist

- [ ] Backend deployed (public URL)
- [ ] Frontend deployed OR document backend-only demo
- [ ] Demo video recorded (5 min)
- [ ] README updated with:
  - [ ] Deployment URL
  - [ ] Architecture diagram
  - [ ] MCP tools list
  - [ ] Datasets used
  - [ ] How to run evals
- [ ] Sample test transcripts
- [ ] Git repo clean and pushed
- [ ] .env.example file (no secrets!)

---

## For Grading/Demo

**Your system demonstrates:**
1. ✅ Voice-based planning (via API)
2. ✅ Voice-based editing (scoped changes)
3. ✅ Grounded explanations (RAG + citations)
4. ✅ 2 MCP tools (POI Search, Itinerary Builder)
5. ✅ 3 Evaluations (Feasibility, Edit, Grounding)
6. ✅ Publicly available datasets (OSM, Wikivoyage)
7. ✅ Feasibility reasoning (not just recommendations)

**Optional bonuses implemented:**
- Hybrid LLM + Symbolic architecture
- 28 curated RAG documents
- Comprehensive evaluation system
- Clean API design
