# 🔴 Current Issue & Quick Fix

## The Problem:

The backend is **using mock data** but the mock POIs only have **placeholder IDs** like `"node/123456"` instead of actual POI information.

### What's Happening:
1. ✅ Groq API works perfectly (tested directly)
2. ❌ Backend LLM call fails silently
3. ❌ Falls back to mock data
4. ❌ Mock data has no POI names - just IDs
5. ❌ Frontend shows empty bullets

---

## Quick Fix Options:

### Option 1: Use Mock Data WITH Names (Fastest)

The backend has POI data like "jaipur_amer_fort", "jaipur_hawa_mahal" but the itinerary builder is generating placeholder IDs instead of using real POIs.

**File to fix:** `backend/data/itinerary_builder_mcp.py`

The issue is the mock itinerary generator creates fake POI IDs (`node/123456`) instead of using actual POIs from the database.

### Option 2: Add Gemini API (Free & Works)

Groq is failing for an unknown reason. Use Google Gemini instead (free, reliable):

1. Get free Gemini key: https://makersuite.google.com/app/apikey
2. Add to `.env`:
   ```env
   GEMINI_API_KEY=your_gemini_key_here
   GEMINI_MODEL=gemini-1.5-flash
   ```
3. Restart backend

---

## What I Recommend:

**FASTEST SOLUTION:** Modify the mock data to return actual POI information instead of placeholder IDs.

The POI database has names like:
- Amer Fort
- Hawa Mahal
- City Palace
- Jantar Mantar

But the itinerary builder creates:
- node/123456
- way/234567
- (no names!)

---

## Files Involved:

1. `backend/data/itinerary_builder_mcp.py` - Generates the itinerary structure
2. `backend/data/poi_search_mcp.py` - Has actual POI data
3. `backend/orchestration/planning_pipeline.py` - Orchestrates everything

The disconnect is that the POI search has real data, but the itinerary builder isn't using it.

---

## Quick Test:

Try adding a Gemini API key as fallback while I investigate the deeper issue.

**Sorry for the frustration!** The issue is more complex than expected - it's not just an API key problem, it's how the backend builds itineraries.
