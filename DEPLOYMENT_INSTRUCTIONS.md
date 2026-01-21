# 🚀 Deployment Instructions

## Quick Start Guide

Your app is ready to deploy! Here's how to get it live in 30 minutes.

---

## Prerequisites

1. GitHub account
2. Vercel account (sign up at vercel.com)
3. Railway account (sign up at railway.app) OR Render account

---

## Step 1: Initialize Git Repository (5 min)

```bash
cd "/Users/newtonschool/Downloads/Grad Project"

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Voice-first AI travel planner

Features:
- Voice-based planning and editing
- Multi-provider LLM with automatic fallback (Grok, Groq, OpenAI, Gemini, Claude)
- Beautiful travel-themed UI with polaroid cards
- AI evaluations (feasibility, edit correctness, grounding)
- RAG with Wikipedia/Wikivoyage/OSM
- Email itineraries
- Sources/references section
- MCP tools (POI Search, Itinerary Builder)"
```

---

## Step 2: Create GitHub Repository (5 min)

### Option A: GitHub Website
1. Go to github.com
2. Click "+" → "New repository"
3. Name: `voyage-travel-planner`
4. Description: `Voice-first AI travel planning assistant with RAG and MCP tools`
5. Keep it Public
6. DON'T initialize with README (you already have one)
7. Click "Create repository"

### Option B: GitHub CLI
```bash
gh repo create voyage-travel-planner --public --source=. --remote=origin
```

### Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/voyage-travel-planner.git
git branch -M main
git push -u origin main
```

---

## Step 3: Deploy Frontend to Vercel (10 min)

### Install Vercel CLI
```bash
npm install -g vercel
```

### Deploy Frontend
```bash
cd frontend

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? voyage-travel-planner
# - Directory? ./
# - Override settings? No
```

### Configure Environment Variables
```bash
# In Vercel dashboard or CLI:
vercel env add NEXT_PUBLIC_API_URL

# Enter the value (your backend URL):
# For now: http://localhost:8000
# Later: https://your-backend-url.railway.app
```

### Deploy to Production
```bash
vercel --prod
```

**Your frontend is now live!** 🎉

---

## Step 4: Deploy Backend to Railway (10 min)

### Option A: Railway Dashboard (Recommended)

1. **Go to railway.app**
2. **Sign in** with GitHub
3. **New Project** → **Deploy from GitHub repo**
4. **Select** your `voyage-travel-planner` repository
5. **Configure Build:**
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`

6. **Add Environment Variables:**
   Click "Variables" tab, add all these:

```env
# LLM API Keys (add at least one)
GROK_API_KEY=your_grok_key
GROQ_API_KEY=your_groq_key
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Models
GROK_MODEL=grok-beta
GROQ_MODEL=llama-3.1-70b-versatile
GEMINI_MODEL=gemini-1.5-flash
OPENAI_MODEL=gpt-3.5-turbo
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Email (optional)
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Backend
BACKEND_PORT=8000
TARGET_CITY=Jaipur
```

7. **Deploy!** Railway will automatically deploy

8. **Get your URL** from Railway dashboard (looks like: `voyage-backend-production.up.railway.app`)

### Option B: Render (Alternative)

1. Go to render.com
2. New → Web Service
3. Connect your GitHub repo
4. Configure:
   - Name: voyage-backend
   - Root Directory: backend
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
5. Add environment variables (same as above)
6. Create Web Service

---

## Step 5: Update Frontend with Backend URL (5 min)

Now that backend is deployed, update frontend:

```bash
cd frontend

# Update environment variable
vercel env add NEXT_PUBLIC_API_URL production

# Enter your Railway/Render URL:
https://your-backend-url.railway.app

# Redeploy
vercel --prod
```

---

## Step 6: Test Deployment (5 min)

1. **Open your Vercel URL**
2. **Test voice input:**
   - Click microphone
   - Say: "Plan a 3-day trip to Jaipur"
3. **Test voice editing:**
   - Say: "Make Day 2 more relaxed"
4. **Test explanations:**
   - Say: "Why did you pick this place?"
5. **Check sources section** appears with citations

**Everything should work!** 🎉

---

## Troubleshooting

### Frontend Issues:

**"Failed to connect to backend"**
- Check `NEXT_PUBLIC_API_URL` is set correctly
- Verify backend is running
- Check CORS settings in backend

**Voice not working**
- Voice only works on HTTPS or localhost
- Vercel provides HTTPS automatically ✅

### Backend Issues:

**"Module not found"**
- Check `requirements.txt` is complete
- Railway/Render may need manual build command

**"No API key found"**
- Verify environment variables are set
- Check spelling (GROK_API_KEY, GROQ_API_KEY, etc.)

**"Port error"**
- Railway assigns port automatically
- Your code should use `PORT` env var or default to 8000

### Quick Fix:
```python
# In main.py, change:
port = int(os.getenv("PORT", os.getenv("BACKEND_PORT", 8000)))
uvicorn.run(app, host="0.0.0.0", port=port)
```

---

## Optional: Custom Domain

### Vercel (Frontend):
1. Go to Vercel dashboard
2. Project settings → Domains
3. Add your domain
4. Follow DNS instructions

### Railway (Backend):
1. Railway dashboard → Settings
2. Add custom domain
3. Update DNS records

---

## Deployment Checklist

- ✅ Git repository initialized
- ✅ Pushed to GitHub
- ✅ Frontend deployed to Vercel
- ✅ Backend deployed to Railway/Render
- ✅ Environment variables set
- ✅ Frontend updated with backend URL
- ✅ Tested voice input
- ✅ Tested voice editing
- ✅ Tested explanations
- ✅ Sources section showing

---

## URLs to Keep

After deployment, save these:

```
GitHub Repo: https://github.com/YOUR_USERNAME/voyage-travel-planner
Frontend URL: https://voyage-travel-planner.vercel.app
Backend URL: https://voyage-backend.railway.app
Demo Video: [YouTube/Drive link]
```

---

## Next Steps

1. **Create Demo Video** (30 min)
   - Use OBS Studio or QuickTime
   - Show all features
   - Upload to YouTube

2. **Update README** with deployment URLs

3. **Submit Project!** 🎉

---

## Cost Breakdown

| Service | Free Tier | Cost |
|---------|-----------|------|
| **Vercel** | ✅ Free forever | $0/mo |
| **Railway** | $5 free credit | ~$5/mo after |
| **Render** | 750 hrs/mo free | $0/mo |
| **Grok API** | Good free tier | $0 |
| **Groq API** | 14,400 req/day | $0 |
| **Gemini API** | 1,500 req/day | $0 |
| **GitHub** | Free public repos | $0 |

**Total:** $0 - $5/month 💰

---

**Your app is production-ready!** 🚀

Need help? Check the troubleshooting section or ask!
