# 🚀 Simple Setup - Just Groq & Gemini

## Step 1: Create .env File

```bash
cd "/Users/newtonschool/Downloads/Grad Project"
cp .env.template .env
nano .env
```

---

## Step 2: Add Your API Keys

Replace `your_groq_key_here` and `your_gemini_key_here` with your actual keys:

```env
# Groq - FIRST PRIORITY
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-70b-versatile

# Gemini - SECOND PRIORITY (Fallback)
GEMINI_API_KEY=your_gemini_key_here
GEMINI_MODEL=gemini-pro

BACKEND_PORT=8000
TARGET_CITY=Jaipur
```

Save: `Ctrl+X`, `Y`, `Enter`

---

## Step 3: Start Backend

```bash
cd backend
python3 main.py
```

---

## Step 4: Start Frontend (New Terminal)

```bash
cd "/Users/newtonschool/Downloads/Grad Project/frontend"
npm run dev
```

---

## Step 5: Open Browser

Go to: **http://localhost:3000**

---

## 🎯 Priority Order:

1. ⚡ **Groq** (Primary - Fast & Free)
2. 🔮 **Gemini** (Fallback)

---

## 📋 Get Your API Keys:

### Groq (You Already Have):
```
your_groq_api_key_here
```

### Gemini (Get Free):
1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy and paste into .env

---

## ✅ Expected Output:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
Attempting LLM call with provider: groq
✅ Successfully using groq!
```

---

**That's it! Just 2 API keys, no confusion!** 🎉
