# Applyt — Full Deployment Guide
### Stack: Neon (DB) · Render (Backend) · Vercel (Frontend) · Firebase (Auth)

---

## Overview

```
User browser
    ↓  HTTPS
Vercel  (React frontend)
    ↓  HTTPS + Bearer token
Render  (FastAPI backend + APScheduler)
    ↓  SSL
Neon    (Postgres database)
    ↓  (token verification)
Firebase Auth
```

---

## Step 1 — Neon Database

1. Sign up at **neon.tech** (free tier is fine)
2. Create a new project, e.g. `applyt`
3. Go to **Connection Details** → copy the **Connection string**
   - It looks like:
     `postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require`
4. **Add the driver prefix** — change `postgresql://` to `postgresql+psycopg2://`
   - Final: `postgresql+psycopg2://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require`
5. Save this — you'll paste it into Render as `DATABASE_URL`

> Tables are created automatically on first backend startup (`Base.metadata.create_all`). No manual SQL needed.

---

## Step 2 — Firebase Authentication

1. Go to **console.firebase.google.com** → Add project
2. **Authentication → Sign-in method** → enable:
   - ✅ Google
   - ✅ Phone
3. **Authentication → Settings → Authorized domains** → Add:
   - Your Vercel domain (e.g. `applyt.vercel.app`)
4. **Project Settings → Your apps → Add app → Web** → register app → copy the config object
5. **Project Settings → Service Accounts → Generate new private key** → download `serviceAccountKey.json`
   - Open it, copy ALL the contents — you'll paste it as `FIREBASE_SERVICE_ACCOUNT_JSON` in Render

---

## Step 3 — Render (Backend)

1. Sign up at **render.com** → New → Web Service → connect your GitHub repo
   - Set **Root Directory** to `app-tracker/backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

2. Add these **Environment Variables** in Render dashboard:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | Your Neon connection string (with `+psycopg2`) |
| `ALLOWED_ORIGINS` | `https://your-app.vercel.app` |
| `FRONTEND_URL` | `https://your-app.vercel.app` |
| `FIREBASE_SERVICE_ACCOUNT_JSON` | Full contents of `serviceAccountKey.json` (paste as one line) |
| `GMAIL_SENDER` | your.email@gmail.com |
| `GMAIL_PASSWORD` | Your 16-char Gmail App Password |

3. Deploy → copy your Render URL (e.g. `https://applyt-api.onrender.com`)

> **Note:** Render free tier spins down after 15 min of inactivity. The first request after sleep takes ~30s. Upgrade to Starter ($7/mo) for always-on. The APScheduler (daily email reminders) runs inside the backend process — it will run reliably on paid tier; on free tier it only runs while the server is awake.

---

## Step 4 — Vercel (Frontend)

1. Sign up at **vercel.com** → New Project → import your GitHub repo
   - Set **Root Directory** to `app-tracker/frontend`
   - Framework: Vite

2. Add these **Environment Variables** in Vercel dashboard:

| Key | Value |
|-----|-------|
| `VITE_API_URL` | `https://applyt-api.onrender.com` (your Render URL) |
| `VITE_FIREBASE_API_KEY` | From Firebase web app config |
| `VITE_FIREBASE_AUTH_DOMAIN` | From Firebase web app config |
| `VITE_FIREBASE_PROJECT_ID` | From Firebase web app config |
| `VITE_FIREBASE_STORAGE_BUCKET` | From Firebase web app config |
| `VITE_FIREBASE_MESSAGING_SENDER_ID` | From Firebase web app config |
| `VITE_FIREBASE_APP_ID` | From Firebase web app config |

3. Deploy → copy your Vercel URL → go back and update `ALLOWED_ORIGINS` and `FRONTEND_URL` in Render

---

## Step 5 — Gmail App Password (for email reminders)

1. Go to **myaccount.google.com/security**
2. Enable **2-Step Verification** if not already on
3. Search **"App passwords"** → Create → name it "Applyt"
4. Copy the 16-character code → paste as `GMAIL_PASSWORD` in Render
5. Set `GMAIL_SENDER` to the same Gmail address

Email reminders are sent to each user's Google account email (phone-only users without an email won't receive reminders).

---

## Local Development

### Backend
```bash
cd app-tracker/backend
cp .env.example .env          # fill in your values
pip install -r requirements.txt
uvicorn main:app --reload
```

You need a local Postgres instance, or point `DATABASE_URL` at your Neon DB directly (works fine for dev).

### Frontend
```bash
cd app-tracker/frontend
cp .env.example .env          # fill in Firebase config + VITE_API_URL
npm install
npm run dev
```

---

## Architecture Notes

- **User isolation**: Every DB row has a `user_id` column (Firebase UID). All queries filter by it — users cannot see each other's data.
- **Auth flow**: Frontend gets a Firebase ID Token → sends it as `Authorization: Bearer <token>` → backend verifies with Firebase Admin SDK → extracts `uid`.
- **Tokens**: Auto-refreshed every 50 minutes on the frontend (they expire after 60 min).
- **Scheduler**: Runs inside the Render web process. Checks for due follow-ups daily at 08:00 server time and emails each user individually.
