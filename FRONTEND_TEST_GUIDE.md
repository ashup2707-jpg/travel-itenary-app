# Frontend Testing Guide

## Fixed Issues ✅

### 1. Voice Input
- ✅ Added proper error handling for microphone access
- ✅ Added console logging for debugging
- ✅ Better browser compatibility check
- ✅ Clear error messages if voice not supported
- ✅ Visual feedback (🎤 when ready, ⏹️ when recording)

### 2. Backend Connection
- ✅ Created `.env.local` with backend URL
- ✅ Added detailed console logging
- ✅ Better error messages showing connection status
- ✅ CORS properly configured in backend

## How to Test

### Step 1: Make sure backend is running
```bash
cd "/Users/newtonschool/Downloads/Grad Project/backend"
python3 main.py
```

You should see:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Start the frontend (in a NEW terminal)
```bash
cd "/Users/newtonschool/Downloads/Grad Project/frontend"
npm run dev
```

You should see:
```
ready - started server on 0.0.0.0:3000, url: http://localhost:3000
```

### Step 3: Open in browser
1. Open Chrome or Edge (Safari doesn't support voice well)
2. Go to: http://localhost:3000
3. Open browser console (F12 or Cmd+Option+I)

### Step 4: Test Voice Input

**Important:** You MUST allow microphone access when prompted!

1. Click the 🎤 microphone button
2. Browser will ask for microphone permission - **click "Allow"**
3. Icon should change to ⏹️ (recording)
4. Speak clearly: "Plan a 3-day trip to Jaipur next weekend"
5. Icon changes back to 🎤
6. Check console logs to see if transcript was captured

**Troubleshooting Voice:**
- If no permission prompt: Check browser settings → Privacy → Microphone
- If error appears: Read the error message (it will tell you what's wrong)
- Check console logs for detailed debugging info

### Step 5: Test Text Input
1. Type in the text box: "Plan a 3-day trip to Jaipur"
2. Click "Send" or press Enter
3. Watch console logs for backend communication
4. Response should appear in chat

### Step 6: Check Console Logs
You should see logs like:
```
Voice recognition started
Transcript: Plan a 3-day trip to Jaipur
Sending to backend: Plan a 3-day trip to Jaipur
API URL: http://localhost:8000
Endpoint: /api/plan
Response status: 200
Backend response: { action: "ask", message: "..." }
```

## Common Issues & Solutions

### Issue: "Voice recognition not supported"
**Solution:** Use Chrome or Edge browser (not Safari or Firefox)

### Issue: "Failed to connect to server"
**Solution:** 
1. Check backend is running: `curl http://localhost:8000/health`
2. Should return: `{"status":"healthy"}`
3. If not, restart backend

### Issue: Microphone not working
**Solution:**
1. Check browser permissions: chrome://settings/content/microphone
2. Make sure your site (localhost:3000) is allowed
3. Try refreshing the page
4. Check if other apps are using the microphone

### Issue: No itinerary showing
**Solution:**
1. Check console logs for errors
2. Make sure backend returned `action: "itinerary"`
3. Check if `result.itinerary.days` exists in response

## What to Look For

### ✅ Working Voice Input:
- Microphone icon changes when clicked
- Browser asks for permission (first time)
- Transcript appears in text box after speaking
- Console shows "Transcript: ..."

### ✅ Working Backend Connection:
- Console shows "Response status: 200"
- Console shows "Backend response: {...}"
- Assistant messages appear in chat
- No red error messages

### ✅ Working Itinerary Display:
- Right panel shows "Day 1", "Day 2", etc.
- Each day has Morning/Afternoon/Evening blocks
- POIs are listed with durations
- Sources section shows citations

## Test Conversation Flow

1. **Initial Request:**
   - Say/Type: "Plan a 3-day trip to Jaipur next weekend"
   - Expected: Assistant asks clarifying questions

2. **Answer Questions:**
   - Say/Type: "I like culture and food, relaxed pace"
   - Expected: More questions or itinerary generation

3. **View Itinerary:**
   - Expected: Right panel shows day-wise plan

4. **Ask Question:**
   - Say/Type: "Why did you pick Hawa Mahal?"
   - Expected: Grounded explanation with sources

5. **Edit Request:**
   - Say/Type: "Make Day 2 more relaxed"
   - Expected: Only Day 2 changes

## Debug Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Browser is Chrome or Edge
- [ ] Microphone permission granted
- [ ] Console open to see logs
- [ ] No CORS errors in console
- [ ] `.env.local` exists in frontend folder
- [ ] Backend shows incoming requests in its logs

## Next Steps After Testing

Once both voice and backend connection work:
1. Test full planning flow
2. Test editing commands
3. Test explanation requests
4. Run evaluations: `curl http://localhost:8000/api/eval/all`
5. Prepare for deployment
