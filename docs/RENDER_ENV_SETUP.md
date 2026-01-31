# 🔐 Render Environment Variables Setup Guide

## Step-by-Step: Adding Environment Variables to Render

---

## 📋 Step 1: Get Your API Keys from Local .env

First, get all your values from your local `.env` file:

```bash
cd "/Users/newtonschool/Downloads/Grad Project"
cat .env
```

**Copy all the values** - you'll paste them into Render in the next steps.

---

## 🌐 Step 2: Navigate to Environment Variables in Render

### 2.1 Go to Your Service
1. Go to: **https://dashboard.render.com**
2. Click on your service: **`travel-planner-backend`**
3. In the left sidebar, click **"Environment"**

### 2.2 You'll See This Section
You'll see a section titled **"Environment Variables"** with:
- A table showing existing variables (if any)
- An **"Add Environment Variable"** button

---

## ➕ Step 3: Add Each Environment Variable

Click **"Add Environment Variable"** for each one below.

### For Each Variable:
1. **Key:** (the name on the left)
2. **Value:** (paste your actual value from `.env`)
3. Click **"Save"**

---

## 📝 Complete List of Environment Variables

### 🔑 LLM API Keys (Add at least ONE)

**1. Groq API Key (Recommended - Fast & Free!)**
```
Key: GROQ_API_KEY
Value: [paste your actual Groq key from .env]
```

**2. OpenAI API Key (Optional)**
```
Key: OPENAI_API_KEY
Value: [paste your actual OpenAI key from .env]
```

**3. Grok API Key (Optional)**
```
Key: GROK_API_KEY
Value: [paste your actual Grok key from .env]
```

**4. Gemini API Key (Optional)**
```
Key: GEMINI_API_KEY
Value: [paste your actual Gemini key from .env]
```

**5. Anthropic API Key (Optional)**
```
Key: ANTHROPIC_API_KEY
Value: [paste your actual Anthropic key from .env]
```

**Note:** You need at least ONE of the above. The app will automatically use whichever is available.

---

### 📧 Email Configuration (Required for Email Feature)

**6. Gmail App Password**
```
Key: SENDER_PASSWORD
Value: [paste your Gmail app password from .env]
```

**7. SMTP Server**
```
Key: SMTP_SERVER
Value: smtp.gmail.com
```

**8. SMTP Port**
```
Key: SMTP_PORT
Value: 587
```

**Note:** Email sender/receiver are hardcoded in the code:
- Sender: `ashup2707@gmail.com`
- Receiver: `f20201480g@alumni.bits-pilani.ac.in`

---

### ⚙️ Backend Configuration (Required)

**9. Port**
```
Key: PORT
Value: 8000
```

**10. Backend Port**
```
Key: BACKEND_PORT
Value: 8000
```

**11. Target City**
```
Key: TARGET_CITY
Value: Jaipur
```

**12. Frontend URL (Update after deploying frontend)**
```
Key: FRONTEND_URL
Value: https://your-frontend-url.vercel.app
```
*(Update this after you deploy frontend to Vercel)*

---

## 🎯 Quick Copy-Paste Template

Here's a template you can use. Replace `[YOUR_VALUE]` with actual values from your `.env`:

```
GROQ_API_KEY=[YOUR_VALUE]
OPENAI_API_KEY=[YOUR_VALUE]
GROK_API_KEY=[YOUR_VALUE]
GEMINI_API_KEY=[YOUR_VALUE]
ANTHROPIC_API_KEY=[YOUR_VALUE]
SENDER_PASSWORD=[YOUR_VALUE]
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
PORT=8000
BACKEND_PORT=8000
TARGET_CITY=Jaipur
FRONTEND_URL=https://placeholder.vercel.app
```

---

## 📸 Visual Guide: Where to Add Variables

### In Render Dashboard:

1. **Service Page** → Click **"Environment"** in left sidebar
2. **Environment Variables Section** → Click **"Add Environment Variable"**
3. **Add Variable Dialog:**
   ```
   ┌─────────────────────────────────┐
   │ Key:   [GROQ_API_KEY        ]   │
   │ Value: [gsk_xxxxxxxxxxxxx    ]   │
   │                                 │
   │        [ Save ]  [ Cancel ]     │
   └─────────────────────────────────┘
   ```
4. Click **"Save"**
5. Repeat for each variable

---

## ✅ Verification Checklist

After adding all variables, verify:

- [ ] At least ONE LLM API key is added (GROQ_API_KEY, OPENAI_API_KEY, etc.)
- [ ] SENDER_PASSWORD is added (for email feature)
- [ ] SMTP_SERVER = `smtp.gmail.com`
- [ ] SMTP_PORT = `587`
- [ ] PORT = `8000`
- [ ] BACKEND_PORT = `8000`
- [ ] TARGET_CITY = `Jaipur`
- [ ] FRONTEND_URL is set (can update later)

---

## 🔍 How to Check Your Variables

### In Render Dashboard:
1. Go to your service
2. Click **"Environment"** tab
3. You'll see all your variables listed (values are hidden for security)

### Test if Variables Are Working:
After deployment, check logs:
1. Go to **"Logs"** tab
2. Look for messages like:
   - `✅ Successfully using groq!` (if GROQ_API_KEY is set)
   - `Email configuration missing` (if SENDER_PASSWORD is missing)

---

## 🐛 Common Issues

### Issue 1: "No LLM API key found"
**Solution:** Add at least one of: GROQ_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY, etc.

### Issue 2: Email not working
**Solution:** 
- Verify SENDER_PASSWORD is set correctly
- Check it's a Gmail App Password (not regular password)
- Verify SMTP_SERVER and SMTP_PORT are set

### Issue 3: Port errors
**Solution:**
- Make sure PORT=8000 is set
- Make sure BACKEND_PORT=8000 is set

### Issue 4: Variables not saving
**Solution:**
- Make sure you click "Save" after adding each variable
- Check for typos in variable names (case-sensitive!)
- Refresh the page and check again

---

## 🔄 After Adding Variables

1. **Render will auto-redeploy** when you add variables
2. **Wait for deployment** to complete (check "Logs" tab)
3. **Test your service** by visiting the URL

---

## 📝 Example: What Your .env File Looks Like

Your local `.env` file should have something like:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
GROK_API_KEY=xai-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SENDER_PASSWORD=xxbxrjtvghgapzyw
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
BACKEND_PORT=8000
TARGET_CITY=Jaipur
```

**Copy these exact values** (without the `KEY=` part) into Render.

---

## 🎯 Quick Steps Summary

1. ✅ Get values from local `.env` file
2. ✅ Go to Render dashboard → Your service → Environment
3. ✅ Click "Add Environment Variable" for each
4. ✅ Copy Key and Value from the list above
5. ✅ Click "Save"
6. ✅ Repeat for all variables
7. ✅ Wait for auto-redeploy
8. ✅ Test your service

---

## 💡 Pro Tips

- **Start with minimum:** Add just GROQ_API_KEY, PORT, BACKEND_PORT, TARGET_CITY first
- **Test deployment:** See if it works with minimal variables
- **Add more later:** Add other API keys and email config after basic deployment works
- **Keep .env safe:** Never commit your local `.env` file (it's already in `.gitignore`)

---

**Need help?** If you get stuck, check the Render logs for specific error messages!
