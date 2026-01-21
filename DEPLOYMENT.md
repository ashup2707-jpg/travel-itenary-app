# 🚀 Deploy to Render - Complete Guide

## Overview
- **Backend:** Deploy to Render (Python/FastAPI)
- **Frontend:** Deploy to Vercel (Next.js) or Render Static Site
- **Time:** ~20 minutes

---

## 📋 Step 1: Prepare Your API Keys

Get all your API keys from your local `.env` file:

```bash
cd "/Users/newtonschool/Downloads/Grad Project"
cat .env
```

**Copy these values** (you'll need them in Step 3):
- `GROQ_API_KEY`
- `OPENAI_API_KEY` (if you have one)
- `GROK_API_KEY` (if you have one)
- `GEMINI_API_KEY` (if you have one)
- `ANTHROPIC_API_KEY` (if you have one)
- `SENDER_PASSWORD` (your Gmail app password)

---

## 🌐 Step 2: Deploy Backend to Render

### 2.1 Create Render Account
1. Go to: **https://render.com**
2. Click **"Get Started for Free"**
3. Sign up with **GitHub** (easiest)
4. Authorize Render to access your repositories

### 2.2 Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Select **"Connect account"** → Choose **GitHub**
3. Find and select: **`ashup2707-jpg/travel-itenary-app`**
4. Click **"Connect"**

### 2.3 Configure Backend Service

**Basic Settings:**
- **Name:** `travel-planner-backend`
- **Environment:** `Python 3`
- **Region:** Choose closest to you (e.g., `Oregon (US West)`)
- **Branch:** `main`
- **Root Directory:** `backend`

**Build & Start:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python3 main.py`

**Plan:**
- Select **"Free"** plan (or paid if you prefer)

### 2.4 Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"** for each:

```env
# LLM API Keys (add the ones you have from your .env file)
GROQ_API_KEY=your_actual_groq_key_here
OPENAI_API_KEY=your_actual_openai_key_here
GROK_API_KEY=your_actual_grok_key_here
GEMINI_API_KEY=your_actual_gemini_key_here
ANTHROPIC_API_KEY=your_actual_anthropic_key_here

# Email Configuration
SENDER_PASSWORD=your_gmail_app_password_here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Backend Configuration
PORT=8000
BACKEND_PORT=8000
TARGET_CITY=Jaipur
FRONTEND_URL=https://your-frontend-url.vercel.app
```

**Important Notes:**
- Add `PORT=8000` (Render uses this automatically, but we set it explicitly)
- Add `BACKEND_PORT=8000` (your code uses this as fallback)
- `FRONTEND_URL` - we'll update this after deploying frontend

### 2.5 Create Service
1. Click **"Create Web Service"**
2. Render will start building automatically
3. Watch the **"Logs"** tab for progress
4. Wait for: **"Your service is live at..."**

### 2.6 Get Backend URL
1. Once deployed, Render will show your service URL
2. Format: `https://travel-planner-backend.onrender.com`
3. **Copy this URL** - you'll need it for frontend

### 2.7 Test Backend
Open the URL in browser or run:
```bash
curl https://your-backend-url.onrender.com/health
```

Should return: `{"status":"healthy"}`

---

## 🎨 Step 3: Deploy Frontend to Vercel

### 3.1 Install Vercel CLI
```bash
npm install -g vercel
```

### 3.2 Login to Vercel
```bash
vercel login
```
- Choose **"GitHub"** to login
- Authorize Vercel

### 3.3 Deploy Frontend
```bash
cd "/Users/newtonschool/Downloads/Grad Project/frontend"
vercel
```

**Follow the prompts:**
1. **Set up and deploy?** → `Y`
2. **Which scope?** → Select your account
3. **Link to existing project?** → `N` (first time)
4. **What's your project's name?** → `travel-planner-frontend`
5. **In which directory is your code located?** → `./` (current directory)
6. **Want to override the settings?** → `N`

Vercel will build and deploy automatically.

### 3.4 Add Environment Variable
1. Go to: **https://vercel.com/dashboard**
2. Click on your project: **`travel-planner-frontend`**
3. Go to **"Settings"** → **"Environment Variables"**
4. Click **"Add New"**
5. Add:
   - **Key:** `NEXT_PUBLIC_API_URL`
   - **Value:** `https://your-backend-url.onrender.com` (from Step 2.6)
   - **Environment:** Production, Preview, Development (check all)
6. Click **"Save"**

### 3.5 Redeploy Frontend
After adding the environment variable, redeploy:

```bash
cd "/Users/newtonschool/Downloads/Grad Project/frontend"
vercel --prod
```

Or trigger a redeploy from Vercel dashboard:
- Go to **"Deployments"** tab
- Click **"..."** on latest deployment → **"Redeploy"**

### 3.6 Get Frontend URL
1. Go to Vercel dashboard
2. Your project → **"Deployments"** tab
3. Click on the latest deployment
4. **Copy the URL** (e.g., `https://travel-planner-frontend.vercel.app`)

### 3.7 Update Backend CORS (if needed)
1. Go back to Render dashboard
2. Your backend service → **"Environment"** tab
3. Update `FRONTEND_URL` to your Vercel URL
4. Render will auto-redeploy

---

## ✅ Step 4: Test Your Deployment

### 4.1 Test Backend
```bash
# Health check
curl https://your-backend-url.onrender.com/health

# Should return: {"status":"healthy"}
```

### 4.2 Test Frontend
1. Open your Vercel URL in browser
2. Try creating an itinerary
3. Check browser console (F12) for any errors

### 4.3 Test API Connection
In browser console, check:
```javascript
// Should show your Render URL
console.log(process.env.NEXT_PUBLIC_API_URL);
```

---

## 🔧 Step 5: Render-Specific Configuration

### 5.1 Render Auto-Deploy
Render automatically deploys when you push to GitHub:
```bash
git add .
git commit -m "Update code"
git push
```
Render will detect the push and redeploy automatically.

### 5.2 Render Free Tier Limitations
- **Spins down after 15 minutes of inactivity**
- **Takes ~30 seconds to wake up** on first request
- **Consider upgrading** if you need always-on service

### 5.3 Render Logs
View logs in Render dashboard:
1. Go to your service
2. Click **"Logs"** tab
3. See real-time logs and errors

---

## 🐛 Troubleshooting

### Backend Not Starting?

**Check Render Logs:**
1. Go to Render dashboard
2. Click on your service
3. Click **"Logs"** tab
4. Look for error messages

**Common Issues:**
- **Missing API key:** Add all required keys to environment variables
- **Port error:** Make sure `PORT=8000` is set in Render
- **Import error:** Check that `requirements.txt` is correct
- **Build timeout:** Free tier has build time limits (upgrade if needed)

### Frontend Can't Connect to Backend?

**Check:**
1. Backend URL is correct in Vercel environment variables
2. Backend is running (check Render logs)
3. CORS is enabled (already done in your code)
4. Backend service is not sleeping (free tier limitation)

**Test CORS:**
```bash
curl -H "Origin: https://your-vercel-url.vercel.app" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     https://your-backend-url.onrender.com/api/plan
```

Should return CORS headers.

### API Keys Not Working?

**Verify:**
1. Keys are correctly pasted (no extra spaces)
2. Keys are active (check provider dashboard)
3. Environment variables are saved in Render
4. Service was redeployed after adding variables

### Backend Sleeping (Free Tier)?

**Solution:**
- First request after 15 min inactivity takes ~30 seconds
- Consider upgrading to paid plan for always-on service
- Or use a service like UptimeRobot to ping your backend every 10 minutes

---

## 📊 Your Deployment URLs

After deployment, you'll have:

- **Backend API:** `https://travel-planner-backend.onrender.com`
- **Frontend:** `https://travel-planner-frontend.vercel.app`

**Update your README.md with these URLs!**

---

## 🎯 Quick Commands Reference

### Render (Backend)
```bash
# View logs
# (Use Render dashboard)

# Redeploy
# (Push to GitHub - Render auto-deploys)
git push
```

### Vercel (Frontend)
```bash
# Deploy
cd frontend
vercel --prod

# View logs
vercel logs

# List deployments
vercel ls
```

---

## ✅ Deployment Checklist

- [ ] Render account created
- [ ] Backend deployed to Render
- [ ] Backend URL copied
- [ ] All API keys added to Render environment variables
- [ ] Backend health check works
- [ ] Vercel account created
- [ ] Frontend deployed to Vercel
- [ ] `NEXT_PUBLIC_API_URL` set in Vercel
- [ ] Frontend URL copied
- [ ] `FRONTEND_URL` updated in Render
- [ ] Frontend can connect to backend
- [ ] Test itinerary creation works
- [ ] Test email sending works (if configured)
- [ ] README updated with deployment URLs

---

## 🔒 Security Best Practices

### ✅ DO:
- ✅ Use environment variables on Render (never hardcode)
- ✅ Never commit `.env` file (already in `.gitignore`)
- ✅ Use different keys for production if possible
- ✅ Rotate keys if exposed

### ❌ DON'T:
- ❌ Hardcode API keys in source code
- ❌ Commit `.env` file
- ❌ Share API keys in screenshots/videos
- ❌ Use same keys for dev and production

---

## 🚀 You're Ready!

Start with **Step 1** above. If you get stuck at any step, let me know and I'll help troubleshoot!

**Estimated Time:** 20-25 minutes total

---

## 📝 Notes

- **Render Free Tier:** Service sleeps after 15 min inactivity (wakes on first request)
- **Auto-Deploy:** Render automatically deploys on git push
- **Environment Variables:** Add them in Render dashboard, not in code
- **Logs:** Always check Render logs if something doesn't work
