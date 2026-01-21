# 🚀 Quick Start Guide - Run Your App

## Step 1: Update .env File with New API Key

```bash
nano .env
```

Find this line:
```env
OPENAI_API_KEY=sk-proj-edkmqNxO...OLD_KEY...
```

Replace with your NEW key:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

Save and exit (Ctrl+X, Y, Enter)

---

## Step 2: Start Backend

```bash
cd backend
python3 main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Leave this terminal running!**

---

## Step 3: Start Frontend (New Terminal)

Open a NEW terminal window:

```bash
cd frontend
npm run dev
```

You should see:
```
ready - started server on 0.0.0.0:3000
```

---

## Step 4: Open in Browser

Go to: **http://localhost:3000**

---

## 🎤 Test Your App

1. **Click the microphone** 🎤 button
2. **Say:** "Plan a 3-day trip to Jaipur. I like food and culture, relaxed pace."
3. **Watch** the itinerary appear!
4. **Try editing:** "Make Day 2 more relaxed"
5. **Ask why:** "Why did you pick this place?"
6. **Check sources** section at the bottom!

---

## ✅ What You Have:

- ✅ Voice-first travel planner
- ✅ Multi-provider LLM (Grok → Groq → **OpenAI** → Gemini → Claude)
- ✅ Beautiful travel-themed UI with polaroid cards
- ✅ Sources section showing Wikipedia/Wikivoyage/OSM
- ✅ Email functionality (📧 Send Email button)
- ✅ AI evaluations
- ✅ RAG with citations

---

## 🐛 Troubleshooting

### "No LLM API key found"
- Make sure you updated `.env` with the new OpenAI key
- Restart the backend server

### "Failed to connect to backend"
- Make sure backend is running on port 8000
- Check backend terminal for errors

### "Voice not working"
- Allow microphone permissions in browser
- Use Chrome or Edge browser

---

## 📋 Next Steps

Once your app is running:

1. ✅ Test all features
2. ✅ Record demo video (5 min)
3. ✅ Deploy to Vercel + Railway
4. ✅ Submit project!

See `DEPLOYMENT_INSTRUCTIONS.md` for deployment guide.

---

**Your app is ready! Start the servers and test it!** 🎉
