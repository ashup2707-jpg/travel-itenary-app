# 🆓 Free API Guide - Maximum Free Tier Usage

## Overview

This guide shows you how to maximize free tier usage across multiple LLM providers. With the right setup, you can get **100,000+ free requests per month**!

---

## 🔥 Recommended Setup (All Free Tiers)

### Priority Order (Best to Fallback):
1. **Grok (xAI)** - First priority ⭐
2. **Groq** - Ultra-fast, generous free tier 🚀
3. **OpenAI** - $5 free credit
4. **Google Gemini** - 60 req/min free
5. **Anthropic Claude** - Limited free tier

---

## 1. 🔥 Grok by xAI (FIRST PRIORITY)

### Why First?
- **From Elon Musk's xAI** - Cutting-edge AI
- **Powerful** - Competitive with GPT-4
- **Good free tier** - Reasonable limits

### Setup:
1. Go to: https://console.x.ai/
2. Sign up with email or GitHub
3. Navigate to API Keys
4. Create new API key
5. Copy the key (starts with `xai-`)

### Add to .env:
```env
GROK_API_KEY=your_grok_api_key_here
GROK_MODEL=grok-beta
```

### Free Tier:
- **Requests:** Check console for current limits
- **Models:** grok-beta, grok-2
- **Speed:** Fast
- **Quality:** Excellent

---

## 2. 🚀 Groq (ULTRA-FAST & FREE)

### Why Use It?
- **FASTEST inference** - 10x faster than competitors!
- **HUGE free tier** - 14,400 requests/day = 432,000/month! 🎉
- **No credit card** required
- **Multiple models** - Llama 3.1, Mixtral, Gemma

### Setup:
1. Go to: https://console.groq.com/
2. Sign up (GitHub/Google)
3. Get API key from dashboard
4. Copy the key (starts with `gsk_`)

### Add to .env:
```env
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=llama-3.1-70b-versatile
```

### Free Tier Limits:
- **14,400 requests/day** (yes, per day!)
- **30 requests/minute**
- **6,000 tokens/minute**
- **No credit card needed**

### Available Models:
```env
# Fastest and most powerful (recommended):
GROQ_MODEL=llama-3.1-70b-versatile

# Ultra-fast for simple tasks:
GROQ_MODEL=llama-3.1-8b-instant

# Great for creative tasks:
GROQ_MODEL=mixtral-8x7b-32768

# Good for coding:
GROQ_MODEL=llama3-groq-70b-8192-tool-use-preview
```

### Performance:
- **Speed:** ⚡ 500+ tokens/second (insanely fast!)
- **Quality:** Excellent (Llama 3.1 70B rivals GPT-4)
- **Cost:** $0 (completely free)

---

## 3. 🤖 OpenAI GPT

### Free Tier:
- **$5 free credit** for new accounts
- **3 months** to use it
- **gpt-3.5-turbo:** ~$0.002 per 1K tokens

### Setup:
1. Go to: https://platform.openai.com/signup
2. Sign up with email
3. Navigate to API Keys
4. Create new secret key
5. Copy the key (starts with `sk-`)

### Add to .env:
```env
OPENAI_API_KEY=sk-proj-your_key_here
OPENAI_MODEL=gpt-3.5-turbo
```

### How Long $5 Lasts:
- **~2.5 million tokens** (input + output)
- **~5,000 planning requests**
- **Good for 1-3 months** of development

---

## 4. 🟢 Google Gemini

### Free Tier:
- **60 requests/minute** (3,600/hour!)
- **1,500 requests/day**
- **1 million tokens/minute**
- **Completely free** - no credit card

### Setup:
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Create API key
4. Copy the key (starts with `AIza`)

### Add to .env:
```env
GEMINI_API_KEY=AIzaSy_your_key_here
GEMINI_MODEL=gemini-1.5-flash
```

### Models:
```env
# Fastest (recommended for free tier):
GEMINI_MODEL=gemini-1.5-flash

# More powerful:
GEMINI_MODEL=gemini-1.5-pro
```

### Free Tier Limits:
- **60 RPM** (requests per minute)
- **1,500 RPD** (requests per day)
- **32K input tokens**
- **8K output tokens**

---

## 5. 🟣 Anthropic Claude

### Free Tier:
- Limited free tier for new accounts
- Very powerful models
- Best for complex reasoning

### Setup:
1. Go to: https://console.anthropic.com/
2. Sign up for account
3. Get API key from settings
4. Copy the key (starts with `sk-ant-`)

### Add to .env:
```env
ANTHROPIC_API_KEY=sk-ant-your_key_here
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

### Models:
```env
# Most cost-effective:
ANTHROPIC_MODEL=claude-3-haiku-20240307

# Balanced (recommended):
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Most powerful:
ANTHROPIC_MODEL=claude-3-opus-20240229
```

---

## 📊 Comparison Table

| Provider | Free Tier | Speed | Quality | Best For |
|----------|-----------|-------|---------|----------|
| **Grok (xAI)** | Good | Fast | Excellent | General use ⭐ |
| **Groq** | 14,400/day! | ⚡ Ultra-fast | Excellent | High volume 🚀 |
| **OpenAI** | $5 credit | Medium | Excellent | Testing |
| **Gemini** | 60/min | Fast | Very Good | Development |
| **Claude** | Limited | Medium | Excellent | Complex tasks |

---

## 💡 Optimal Strategy

### For Maximum Free Usage:

```env
# 1. Primary: Grok (xAI) - Your key provided ⭐
GROK_API_KEY=your_grok_api_key_here

# 2. Fallback: Groq - Get this NOW! 14,400 free requests/day! 🚀
GROQ_API_KEY=gsk_your_key_here

# 3. Fallback: Gemini - 1,500 requests/day
GEMINI_API_KEY=AIza_your_key_here

# 4. Fallback: OpenAI - $5 credit
OPENAI_API_KEY=sk-proj_your_key_here

# 5. Final Fallback: Claude
ANTHROPIC_API_KEY=sk-ant_your_key_here
```

### Expected Total Free Capacity:
- **Groq alone:** 14,400 req/day = **432,000/month** 🎉
- **Gemini:** 1,500 req/day = 45,000/month
- **Combined:** 470,000+ requests/month for FREE!

---

## 🆓 More Free API Options

### 6. Together AI
- **Website:** https://together.ai/
- **Free Tier:** $25 free credit
- **Models:** Llama 2, Mixtral, many open-source models
- **API:** OpenAI-compatible

### 7. Perplexity API
- **Website:** https://www.perplexity.ai/
- **Free Tier:** Limited free requests
- **Models:** pplx-7b, pplx-70b
- **Bonus:** Web search integration

### 8. Mistral AI
- **Website:** https://console.mistral.ai/
- **Free Tier:** €5 free credit
- **Models:** Mistral-7B, Mixtral-8x7B
- **API:** OpenAI-compatible

### 9. Cohere
- **Website:** https://cohere.com/
- **Free Tier:** Trial credits available
- **Models:** Command, Command Light
- **Good for:** Text generation, embeddings

### 10. Hugging Face Inference API
- **Website:** https://huggingface.co/inference-api
- **Free Tier:** Rate-limited free tier
- **Models:** 1000+ open-source models
- **Flexibility:** Try different models

---

## 🎯 How to Add Your Grok Key

Since you provided your Grok API key, here's how to use it:

### Option 1: Add to .env file
```bash
# In your .env file:
GROK_API_KEY=your_grok_api_key_here
```

### Option 2: Use environment variable
```bash
export GROK_API_KEY=your_grok_api_key_here
```

### Then start your backend:
```bash
cd backend
python3 main.py
```

**It will automatically use Grok as the first priority!** ⭐

---

## 🚀 Quick Setup Command

Create your `.env` file with all providers:

```bash
cat > .env << 'EOF'
# PRIMARY: Grok (xAI) ⭐
GROK_API_KEY=your_grok_api_key_here
GROK_MODEL=grok-beta

# FALLBACK 1: Groq (GET THIS - 14,400 FREE/DAY!) 🚀
GROQ_API_KEY=
GROQ_MODEL=llama-3.1-70b-versatile

# FALLBACK 2: Gemini
GEMINI_API_KEY=
GEMINI_MODEL=gemini-1.5-flash

# FALLBACK 3: OpenAI
OPENAI_API_KEY=
OPENAI_MODEL=gpt-3.5-turbo

# FALLBACK 4: Claude
ANTHROPIC_API_KEY=
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Email (optional)
SENDER_EMAIL=
SENDER_PASSWORD=

# Backend
BACKEND_PORT=8000
EOF
```

---

## 📈 Usage Monitoring

### Check which provider is being used:
Watch your backend console logs:
```
Attempting LLM call with provider: grok
✓ Success with grok

# If rate limit hit:
Rate limit hit on grok
Falling back to next provider...
Attempting LLM call with provider: groq
✓ Success with groq
```

---

## 🎯 Recommendation

**Get Groq API key IMMEDIATELY!**
- Takes 2 minutes to sign up
- No credit card needed
- 14,400 requests/day = **432,000/month FREE**
- 10x faster than other providers
- Perfect fallback for your Grok key

**Link:** https://console.groq.com/ 🚀

---

## ⚠️ Important Notes

1. **Never commit API keys** to git
2. **Rotate keys** if exposed publicly
3. **Monitor usage** in provider dashboards
4. **Respect rate limits** - our app handles this automatically
5. **Free tiers can change** - check provider websites for current limits

---

**Your Grok key is now set as FIRST PRIORITY!** ⭐

The app will use it first, then fallback to others if needed.

**Last Updated:** January 21, 2026
