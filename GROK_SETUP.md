# 🔥 Grok API Setup - Quick Guide

Your Grok API key has been integrated as the **FIRST PRIORITY** provider!

---

## ✅ What's Been Done

1. ✅ Grok (xAI) added to LLM client
2. ✅ Set as **FIRST PRIORITY** provider
3. ✅ Groq added as second priority (ultra-fast, 14,400 free/day!)
4. ✅ All other providers as fallbacks
5. ✅ Your API key ready to use

---

## 🚀 Quick Setup

### 1. Add Your Grok Key to .env

```bash
# Create/edit .env file
cat > .env << 'EOF'
# PRIMARY: Grok (xAI) - YOUR KEY ⭐
GROK_API_KEY=your_grok_api_key_here
GROK_MODEL=grok-beta

# HIGHLY RECOMMENDED: Get Groq (14,400 free requests/day!) 🚀
GROQ_API_KEY=
GROQ_MODEL=llama-3.1-70b-versatile

# Other providers (optional fallbacks)
GEMINI_API_KEY=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

# Email (optional)
SENDER_EMAIL=
SENDER_PASSWORD=

# Backend
BACKEND_PORT=8000
EOF
```

### 2. Start Backend

```bash
cd backend
python3 main.py
```

You should see:
```
Attempting LLM call with provider: grok
✓ Using Grok (xAI) as primary provider
```

### 3. Test It

```bash
cd frontend
npm run dev
```

Open http://localhost:3000 and create an itinerary!

---

## 🎯 Priority Order (How It Works)

When you make a request:

1. **First:** Tries **Grok** (your key) ⭐
2. **If rate limit:** Tries **Groq** (if configured)
3. **If rate limit:** Tries **Gemini** (if configured)
4. **If rate limit:** Tries **OpenAI** (if configured)
5. **If rate limit:** Tries **Anthropic** (if configured)

**You'll never see an error** - automatic fallback handles everything!

---

## 📊 Your Current Setup

### Grok API Key
```
✅ Configured: your_grok_api_key_here
✅ Priority: FIRST
✅ Model: grok-beta
```

### Recommended Next Step
Get **Groq API key** for fallback:
- **Free:** 14,400 requests/day
- **Fast:** 10x faster than competitors
- **Easy:** 2-minute signup
- **Link:** https://console.groq.com/

---

## 🔍 Monitoring

### Check Backend Logs

When you make requests, you'll see:
```bash
Attempting LLM call with provider: grok
✓ Success with grok

# If rate limit hit:
Rate limit hit on grok: 429 error
Falling back to next provider...
Attempting LLM call with provider: groq
✓ Success with groq
Switched primary provider from grok to groq
```

---

## 🎨 Available Grok Models

```env
# Latest beta (recommended):
GROK_MODEL=grok-beta

# Grok 2 (when available):
GROK_MODEL=grok-2

# Check https://console.x.ai/ for latest models
```

---

## ⚡ Performance Comparison

| Provider | Speed | Quality | Free Tier |
|----------|-------|---------|-----------|
| **Grok** ⭐ | Fast | Excellent | Good |
| **Groq** 🚀 | Ultra-fast | Excellent | 14,400/day |
| Gemini | Fast | Very Good | 1,500/day |
| OpenAI | Medium | Excellent | $5 credit |
| Claude | Medium | Excellent | Limited |

---

## 💡 Pro Tips

### 1. Add Groq for Maximum Reliability
With both Grok + Groq, you get:
- **Primary:** Grok (powerful, good limits)
- **Fallback:** Groq (ultra-fast, 14,400/day)
- **Result:** Virtually unlimited free usage!

### 2. Monitor Usage
Check your usage at:
- **Grok:** https://console.x.ai/
- **Groq:** https://console.groq.com/

### 3. Set Up Email
Once you have itineraries working, configure email:
```env
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_gmail_app_password
```

---

## 🐛 Troubleshooting

### Grok Not Working?

**Check 1:** Verify .env file
```bash
cat .env | grep GROK
```
Should show:
```
GROK_API_KEY=xai-ycKyq...
```

**Check 2:** Restart backend
```bash
cd backend
python3 main.py
```

**Check 3:** Look at logs
```bash
# Should see:
Attempting LLM call with provider: grok
```

### Still Not Working?

1. **Check API key** at https://console.x.ai/
2. **Verify quota** in xAI console
3. **Check logs** for specific error messages
4. **Try fallback** - add Groq key to test system

---

## 📞 Getting More Help

1. **Check logs** - backend shows detailed error messages
2. **Verify .env** - make sure GROK_API_KEY is set
3. **Test connection** - try simple request first
4. **Add fallback** - set up Groq as backup

---

## 🚀 Next Steps

### Immediate (5 minutes):
1. ✅ Add your Grok key to `.env` (done above)
2. ✅ Start backend and frontend
3. ✅ Test with a simple itinerary request

### Recommended (2 minutes):
1. 🚀 Get **Groq** API key: https://console.groq.com/
2. 📧 Set up **email** for sending itineraries
3. 📊 Monitor usage in xAI console

### Optional (10 minutes):
1. Add Gemini key (1,500 free/day)
2. Add OpenAI key ($5 credit)
3. Set up all 5 providers for maximum reliability

---

## 🎉 You're All Set!

Your **Grok API** is configured as **FIRST PRIORITY**!

Just run:
```bash
cd backend && python3 main.py
```

And start planning trips with Grok! ⭐

---

**For more free API options, see:** `FREE_API_GUIDE.md`

**Last Updated:** January 21, 2026
