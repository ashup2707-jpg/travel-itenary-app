# 🚀 Add Your Groq API Key

## Your Groq Key:
```
YOUR_GROQ_API_KEY_HERE
```

## How to Add It:

### 1. Edit .env File

```bash
cd "/Users/newtonschool/Downloads/Grad Project"
nano .env
```

### 2. Add This Line at the Top:

```env
# Groq API (FIRST PRIORITY - Fast & Free!)
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-70b-versatile

# OpenAI (Second Priority)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Grok (Third Priority - requires credits)
GROK_API_KEY=your_grok_key_here
GROK_MODEL=grok-beta
```

Save and exit (Ctrl+X, Y, Enter)

---

## 3. Restart Backend

```bash
cd backend
python3 main.py
```

---

## ✅ Expected Output:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
Attempting LLM call with provider: groq
✅ Successfully using groq!
```

---

## 🎯 New Priority Order:

1. ⚡ **Groq** ← YOUR KEY (First choice!)
2. 🤖 OpenAI (Fallback)
3. 🦎 Grok (Fallback - no credits)
4. 🔮 Gemini (Fallback)
5. 🧠 Anthropic (Fallback)

---

## Why Groq is Awesome:

- ✅ **FREE** generous limits
- ⚡ **SUPER FAST** (10x faster than GPT)
- 🔥 **RELIABLE** - no rate limits
- 💪 **POWERFUL** - Llama 3.1 70B model

---

**Add the key to .env and restart the backend!** Your itinerary will generate perfectly! 🚀
