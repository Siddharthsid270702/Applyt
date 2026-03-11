# Applyt — Job Application Tracker

A full-stack web app to track your job applications, notes, and follow-ups.

## Tech Stack

- **Frontend** — React + Vite, hosted on Vercel
- **Backend** — FastAPI (Python), hosted on Vercel Serverless
- **Database** — Neon (PostgreSQL)
- **Auth** — Firebase Authentication (Google Sign-in)

---

## Project Structure

```
app-tracker/
├── frontend/          # React app
│   ├── src/
│   │   ├── components/
│   │   ├── api/
│   │   ├── App.jsx
│   │   ├── AuthContext.jsx
│   │   └── firebase.js
│   ├── .env
│   └── package.json
│
└── backend/           # FastAPI app
    ├── app/
    │   ├── routers/
    │   ├── auth.py
    │   ├── crud.py
    │   ├── database.py
    │   ├── models.py
    │   └── schemas.py
    ├── api/
    │   └── index.py
    ├── main.py
    ├── vercel.json
    ├── .env
    └── requirements.txt
```

---

## Local Development

### Prerequisites
- Python 3.10+
- Node.js 18+
- A [Neon](https://neon.tech) database
- A [Firebase](https://console.firebase.google.com) project with Google Auth enabled

### Backend

```bash
cd app-tracker/backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd app-tracker/frontend
npm install
npm run dev
```

---

## Environment Variables

### Backend `.env`

```env
DATABASE_URL=postgresql+psycopg2://user:pass@ep-xxx.neon.tech/neondb?sslmode=require
ALLOWED_ORIGINS=http://localhost:5173
FRONTEND_URL=http://localhost:5173
FIREBASE_SERVICE_ACCOUNT_PATH=serviceAccountKey.json
GMAIL_SENDER=your@gmail.com
GMAIL_PASSWORD=your-app-password
```

### Frontend `.env`

```env
VITE_API_URL=http://127.0.0.1:8000
VITE_FIREBASE_API_KEY=
VITE_FIREBASE_AUTH_DOMAIN=
VITE_FIREBASE_PROJECT_ID=
VITE_FIREBASE_STORAGE_BUCKET=
VITE_FIREBASE_MESSAGING_SENDER_ID=
VITE_FIREBASE_APP_ID=
```

---



- Google Sign-in authentication
- Each user sees only their own data
- Add, update, and delete job applications
- Track application status
- Add notes per application
- Schedule follow-up reminders
- Archive and restore applications
