# Authentication Setup Guide

This version of Applyt uses **Firebase Authentication** to give each user their own isolated data.  
Supported sign-in methods: **Google** and **Phone Number**.

---

## 1 · Create a Firebase Project

1. Go to [console.firebase.google.com](https://console.firebase.google.com) and click **Add project**.
2. Enable **Authentication** → **Sign-in method**:
   - Turn on **Google**
   - Turn on **Phone**
3. Add your frontend domain to **Authorized domains** (e.g. `your-app.vercel.app`).

---

## 2 · Frontend — Firebase client config

In **Firebase Console → Project Settings → Your apps → Web app** copy the config object.

Create `frontend/.env` (copy from `.env.example`):

```
VITE_API_URL=https://your-backend.onrender.com

VITE_FIREBASE_API_KEY=AIza...
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789
VITE_FIREBASE_APP_ID=1:123:web:abc
```

Install dependencies:
```bash
cd frontend
npm install      # installs firebase + existing deps
npm run dev
```

---

## 3 · Backend — Firebase Admin SDK

1. In Firebase Console → **Project Settings → Service Accounts** → click **Generate new private key**.  
   This downloads a `serviceAccountKey.json` file.

2. Create `backend/.env` (copy from `.env.example`) and set **one** of:

**Option A — JSON string** (recommended for Render/cloud):
```
FIREBASE_SERVICE_ACCOUNT_JSON={"type":"service_account","project_id":"..."}
```
Paste the entire contents of `serviceAccountKey.json` as the value (single line, keep the JSON).

**Option B — file path** (local dev):
```
FIREBASE_SERVICE_ACCOUNT_PATH=/absolute/path/to/serviceAccountKey.json
```

3. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 4 · Database migration

The `applications` and `archived_applications` tables now have a `user_id VARCHAR(128)` column.

**Fresh database** — no action needed; `Base.metadata.create_all` will create tables with the new column on first run.

**Existing database** — run this SQL before deploying:
```sql
ALTER TABLE applications          ADD COLUMN user_id VARCHAR(128) NOT NULL DEFAULT '' AFTER id;
ALTER TABLE archived_applications ADD COLUMN user_id VARCHAR(128) NOT NULL DEFAULT '' AFTER id;
CREATE INDEX ix_applications_user_id          ON applications(user_id);
CREATE INDEX ix_archived_applications_user_id ON archived_applications(user_id);
```

> Existing rows will have `user_id = ''` — they won't be visible to any logged-in user.  
> You can delete them or manually assign them to a user's Firebase UID.

---

## 5 · How it works

```
User signs in (Google or Phone)
      ↓
Firebase issues an ID Token (JWT, valid 60 min)
      ↓
Frontend axios interceptor attaches:
  Authorization: Bearer <id-token>
      ↓
FastAPI verifies token with Firebase Admin SDK
  → extracts uid (unique per user)
      ↓
All DB queries filter by uid
  → each user sees only their own data
```

---

## 6 · Phone auth note

Firebase Phone Authentication sends an **SMS verification code** to the user.  
The sign-in flow in this app:

1. User enters their phone number with country code (e.g. `+91 98765 43210`)
2. Firebase sends an SMS with a 6-digit code
3. User enters the code → signed in

This is the standard Firebase phone auth flow; there is no way to completely skip the SMS step since it is how Firebase verifies phone ownership.  
If you want a truly code-free phone sign-in, consider using phone number as a profile field only and requiring Google as the auth provider.

---

## 7 · Deployment checklist

| Item | Where |
|------|-------|
| Firebase web config vars (`VITE_*`) | Vercel / Netlify environment variables |
| `FIREBASE_SERVICE_ACCOUNT_JSON` | Render secret environment variable |
| Frontend domain added to Firebase Authorized Domains | Firebase Console → Auth → Settings |
| `ALLOWED_ORIGINS` includes frontend URL | Render env var |
