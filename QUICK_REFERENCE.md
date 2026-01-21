# Quick Reference Guide

## 🎯 What Was Added

### 1. Multi-Provider LLM Fallback ✅
**No more API failures!** Automatically switches between OpenAI, Gemini, and Anthropic.

### 2. Email Sender ✅
**Send itineraries** to up to 2 (or more) email addresses with beautiful HTML formatting.

### 3. Voice Features (Already Had) ✅
**Browser-native** speech-to-text and text-to-speech - completely free!

---

## 📋 Setup Checklist

### Minimal Setup (Just to Run)
```env
# Add to .env file - need at least ONE:
GEMINI_API_KEY=your_key_here
```

### Recommended Setup (With Fallback)
```env
# Priority order - add all for maximum reliability:
GROK_API_KEY=your_grok_key_here          # First priority ⭐
GROQ_API_KEY=your_groq_key_here          # 14,400 free/day! 🚀
GEMINI_API_KEY=your_gemini_key_here
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

### Full Setup (All Features)
```env
# LLM providers (all three recommended)
OPENAI_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Email (optional but recommended)
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_gmail_app_password
```

---

## 🚀 Quick Start

```bash
# 1. Setup environment
cp env.template .env
# Edit .env with your API keys

# 2. Start backend
cd backend
python3 main.py

# 3. Start frontend (new terminal)
cd frontend
npm run dev

# 4. Open browser
# http://localhost:3000
```

---

## 🎤 How to Use Voice

1. Click **🎤** microphone button
2. Allow microphone access (if prompted)
3. Speak: *"Plan a 3-day trip to Jaipur"*
4. Listen to assistant's voice response

**No setup needed** - works automatically in Chrome/Edge!

---

## 📧 How to Send Email

1. Create an itinerary
2. Click **📧 Send Email** button (top right)
3. Enter email addresses (up to 2)
4. Click **Send Email**
5. Done! Recipients get beautiful HTML email

---

## 🔑 Get API Keys

| Provider | Free Tier | Get Key |
|----------|-----------|---------|
| **Grok (xAI)** ⭐ | Good limits | https://console.x.ai/ |
| **Groq** 🚀 | **14,400/day!** | https://console.groq.com/ |
| **Gemini** | Yes (60 req/min) | https://makersuite.google.com/app/apikey |
| **OpenAI** | $5 credit | https://platform.openai.com/api-keys |
| **Anthropic** | Limited free | https://console.anthropic.com/ |

**🔥 Get Groq first - 14,400 free requests/day = 432,000/month!**

---

## 📧 Gmail App Password Setup

1. Go to: https://myaccount.google.com/apppasswords
2. Enable **2-Step Verification** (required)
3. Create App Password:
   - App: **Mail**
   - Device: **Other** (type "Voyage App")
4. Copy the 16-character password
5. Add to `.env`:
   ```env
   SENDER_EMAIL=your_email@gmail.com
   SENDER_PASSWORD=abcd efgh ijkl mnop
   ```

**Important:** Use App Password, NOT your regular Gmail password!

---

## 🔄 How Fallback Works

```
Request → Try Grok (xAI) ⭐
           ↓ (rate limit)
         Try Groq 🚀
           ↓ (rate limit)
         Try Gemini
           ↓ (rate limit)
         Try OpenAI
           ↓ (rate limit)
         Try Anthropic
           ↓
         Success!
```

**Automatic.** You won't even notice when it switches! 🎉

With **Groq's 14,400 requests/day**, you'll rarely hit rate limits!

---

## 📊 What You Asked vs What You Got

✅ **Understand STT/TTS** → Documented (browser APIs, not ElevenLabs, 100% free)  
✅ **Multi-layer API fallback** → 3 providers with automatic switching  
✅ **Email sender (2 emails)** → Beautiful HTML emails, up to 10 recipients  

---

## 🐛 Troubleshooting

### Email Not Sending?
- Gmail: Use **App Password** (not regular password)
- Enable **2-Step Verification** in Google Account
- Check `.env` has `SENDER_EMAIL` and `SENDER_PASSWORD`

### API Rate Limit?
- Add more API keys → automatic fallback handles it
- Check backend logs → see which provider is being used

### Voice Not Working?
- Use **Chrome or Edge** browser
- Allow **microphone access**
- Check **system volume**

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `env.template` | Configuration template (copy to `.env`) |
| `IMPLEMENTATION_SUMMARY.md` | Complete feature documentation |
| `FEATURE_UPDATES.md` | Detailed technical docs |
| `README.md` | Main project documentation |
| `QUICK_REFERENCE.md` | This file! |

---

## 💡 Pro Tips

1. **Add all 3 API keys** for best reliability
2. **Gmail App Password** is must for email feature
3. **Chrome/Edge** for best voice experience
4. **Check backend logs** to see provider switching
5. **Use free tiers** of all providers to maximize quota

---

## 📞 Need Help?

1. Check `IMPLEMENTATION_SUMMARY.md` for detailed setup
2. Check `FEATURE_UPDATES.md` for technical details
3. Check backend console logs for error messages
4. Verify `.env` file has correct configuration

---

**Everything is ready to go!** 🚀

Just add your API keys to `.env` and start the servers.

---

**Last Updated:** January 21, 2026  
**Status:** All features working ✅
