# 🔧 Fix & Run - Quick Steps

## Issue: OpenAI Library Version Incompatibility

The backend crashed due to an outdated OpenAI library. Here's how to fix it:

---

## Step 1: Update OpenAI API Key in .env

```bash
cd "/Users/newtonschool/Downloads/Grad Project"
nano .env
```

Find and replace the OpenAI key:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

Save (Ctrl+X, Y, Enter)

---

## Step 2: Upgrade Python Packages

```bash
cd backend

# Upgrade pip first
python3 -m pip install --upgrade pip --user

# Upgrade OpenAI and dependencies
python3 -m pip install --upgrade openai httpx anthropic --user

# Verify installation
python3 -c "import openai; print(f'OpenAI version: {openai.__version__}')"
```

You should see: `OpenAI version: 2.x.x` (anything 2.0 or higher is good)

---

## Step 3: Start Backend

```bash
cd backend
python3 main.py
```

**Expected output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **Leave this terminal running!**

---

## Step 4: Start Frontend (New Terminal)

Open a NEW terminal:

```bash
cd "/Users/newtonschool/Downloads/Grad Project/frontend"
npm run dev
```

**Expected output:**
```
ready - started server on 0.0.0.0:3000, url: http://localhost:3000
```

---

## Step 5: Test in Browser

1. Open: **http://localhost:3000**
2. You should see the beautiful travel-themed UI
3. Click 🎤 microphone
4. Say: "Plan a 3-day trip to Jaipur"
5. Watch the magic! ✨

---

## 🐛 If Backend Still Crashes

### Check Python Version:
```bash
python3 --version
```

Should be **Python 3.9+**

### Try Virtual Environment:
```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run
python3 main.py
```

---

## ✅ What Should Work:

Once both servers are running:

1. ✅ Voice input/output (browser-native)
2. ✅ Multi-provider LLM fallback:
   - Priority: Grok → Groq → **OpenAI** → Gemini → Claude
3. ✅ Beautiful UI with polaroid cards
4. ✅ Sources section showing Wikipedia/Wikivoyage
5. ✅ Email functionality
6. ✅ Voice editing
7. ✅ Explanations with citations

---

## 🎬 Next Steps

Once working:

1. ✅ **Test thoroughly** - Try all features
2. ✅ **Record demo video** - 5 minutes showing:
   - Voice planning
   - Voice editing
   - Explanations
   - Sources section
   - Running evaluation
3. ✅ **Deploy** - See `DEPLOYMENT_INSTRUCTIONS.md`
4. ✅ **Submit!** 🎉

---

## 📞 Still Having Issues?

Common fixes:

**"Port 8000 already in use":**
```bash
lsof -ti:8000 | xargs kill -9
```

**"Module not found":**
```bash
pip3 install -r requirements.txt --user
```

**"Permission denied":**
```bash
# Use --user flag
pip3 install --upgrade openai --user
```

---

**Your app is almost ready! Just upgrade those packages and run!** 🚀
