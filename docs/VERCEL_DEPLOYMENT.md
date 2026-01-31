# Deploy Frontend to Vercel

Step-by-step guide to deploy the Next.js frontend to Vercel, with troubleshooting.

---

## Prerequisites

- Backend deployed (e.g. Render): e.g. `https://travel-itenary-app.onrender.com`
- Node.js installed
- Git repository pushed to GitHub (optional; you can deploy without linking)

---

## 1. Install / Use Vercel CLI

**Option A — Use npx (recommended, no global install):**

```bash
cd frontend
npx vercel login
npx vercel
npx vercel --prod   # when ready for production
```

**Option B — Global install:**

```bash
npm install -g vercel
vercel --version
vercel login
```

If you get `EACCES: permission denied`, use **Option A** (npx) instead.

---

## 2. Deploy

```bash
cd "/path/to/Grad Project/frontend"
npx vercel
```

Answer prompts:

- Set up and deploy? → **Y**
- Which scope? → Your account
- Link to existing project? → **N** (first time)
- Project name? → e.g. `travel-planner-frontend`
- Directory? → `./`
- Override settings? → **N**

---

## 3. Environment Variable (Vercel)

1. Vercel Dashboard → your project → **Settings** → **Environment Variables**.
2. Add:
   - **Key:** `NEXT_PUBLIC_API_URL`
   - **Value:** `https://travel-itenary-app.onrender.com` (your backend URL)
   - **Environments:** Production, Preview, Development.
3. Save.

---

## 4. Backend CORS (Render)

In Render: **Environment** → set **`FRONTEND_URL`** to your Vercel URL (e.g. `https://travel-planner-frontend.vercel.app`). Save; Render will redeploy.

---

## 5. Redeploy Frontend

```bash
cd frontend
npx vercel --prod
```

Or in Vercel Dashboard: Deployments → … → Redeploy.

---

## 6. Verify

- Open the Vercel URL and confirm the UI loads.
- Create an itinerary (e.g. “Plan a 3-day trip to Jaipur”).
- Check browser console and Network tab for errors or CORS issues.

---

## Troubleshooting

### Git author / team access error

If you see: `Git author ... must have access to the team`:

1. Remove link to existing project:
   ```bash
   cd frontend
   rm -rf .vercel
   ```
2. Deploy as new project: `npx vercel`, and when asked **Link to existing project?** choose **N**.

### Frontend can’t connect to backend

- Confirm `NEXT_PUBLIC_API_URL` in Vercel matches the backend URL.
- Confirm `FRONTEND_URL` in Render matches the Vercel URL.
- Check backend is up: open `https://your-backend.onrender.com/health`.
- On free tier, backend may sleep; wait ~30 s after first request.

### Build fails

- Check Vercel build logs for missing deps or TypeScript errors.
- Run locally: `npm run build` in `frontend` and fix any errors, then push and redeploy.

### “vercel: command not found”

Use npx: `npx vercel` (and `npx vercel login`, `npx vercel --prod`) so no global install is needed.

---

## Quick reference

```bash
npx vercel login
npx vercel          # first deploy
npx vercel --prod   # production
npx vercel ls       # list deployments
npx vercel logs     # view logs
```
