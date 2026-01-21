# 🔧 Complete .env Setup - Fix All API Keys

## Problem:
- Groq key is missing from .env
- Old OpenAI key is still there (should be the new one)
- Backend needs restart

---

## Step 1: Edit .env File

```bash
cd "/Users/newtonschool/Downloads/Grad Project"
nano .env
```

---

## Step 2: Replace ENTIRE .env Contents with This:

```env
# ============================================
# LLM API KEYS (Priority Order)
# ============================================

# 1. Groq - FIRST PRIORITY (Fast & Free!)
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-70b-versatile

# 2. OpenAI - Second Priority
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# 3. Grok (xAI) - Third Priority (no credits)
# GROK_API_KEY=your_grok_key_here
# GROK_MODEL=grok-beta

# 4. Google Gemini (Optional)
# GEMINI_API_KEY=your_key_here
# GEMINI_MODEL=gemini-pro

# 5. Anthropic Claude (Optional)
# ANTHROPIC_API_KEY=your_key_here
# ANTHROPIC_MODEL=claude-3-haiku-20240307

# ============================================
# Email Configuration (Optional)
# ============================================
# SENDER_EMAIL=your_email@gmail.com
# SENDER_PASSWORD=your_app_password
# SMTP_SERVER=smtp.gmail.com
# SMTP_PORT=587

# ============================================
# Backend Configuration
# ============================================
BACKEND_PORT=8000
TARGET_CITY=Jaipur
```

**Save and Exit:** Press `Ctrl+X`, then `Y`, then `Enter`

---

## Step 3: Restart Backend

```bash
# Stop current backend (Ctrl+C in terminal 9)

cd backend
python3 main.py
```

---

## ✅ Expected Output (Correct!):

```
INFO:     Uvicorn running on http://0.0.0.0:8000
Attempting LLM call with provider: groq    ← Should say GROQ first!
✅ Using groq successfully!
```

---

## ❌ Current Output (Wrong!):

```
Attempting LLM call with provider: openai    ← Wrong! Should be groq
⚠️ LLM parsing failed: Error code: 401...    ← Old API key
```

---

## 🎯 What This Fixes:

1. ✅ Adds Groq API key (first priority)
2. ✅ Updates OpenAI to NEW key (ends with qMQA)
3. ✅ Removes old broken keys
4. ✅ Proper priority order

---

## 📋 Quick Command Summary:

```bash
# 1. Edit .env
nano .env

# 2. Paste the complete .env contents above

# 3. Save (Ctrl+X, Y, Enter)

# 4. Restart backend
cd backend
python3 main.py

# 5. Test in browser
# Refresh http://localhost:3000 and try again
```

---

**Do this now and your itinerary will generate perfectly with Groq!** 🚀
