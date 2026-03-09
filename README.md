# 📋 Job Application Tracker

Full-stack job application tracker — FastAPI backend + React frontend.

---

## 🗂 Project Structure

```
app-tracker/
├── backend/          ← FastAPI + PostgreSQL
│   ├── main.py
│   ├── requirements.txt
│   ├── .env                ← fill in your DB URL
│   └── app/
│       ├── database.py
│       ├── models.py
│       ├── schemas.py
│       ├── crud.py
│       ├── enums.py
│       ├── scheduler.py
│       └── routers/
│           └── application.py
│
└── frontend/         ← React + Vite
    ├── index.html
    ├── package.json
    ├── vite.config.js
    ├── .env                ← set VITE_API_URL
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── App.module.css
        ├── styles/
        │   └── globals.css
        ├── api/
        │   └── api.js
        └── components/
            ├── Sidebar
            ├── StatCards
            ├── ApplicationList
            ├── ApplicationForm
            ├── DetailDrawer
            ├── Notes
            ├── Followups
            ├── ArchivedApplications
            └── StatusPill
```

---

## ⚡ Local Setup (MySQL via XAMPP)

### 1. Start XAMPP MySQL

1. Open **XAMPP Control Panel**
2. Click **Start** next to **MySQL**
3. Click **Admin** (or open `http://localhost/phpmyadmin`)
4. Click **New** → type `application_tracker` → click **Create**

### 2. Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# .env is already configured for XAMPP (no password needed by default)
# If you have a MySQL password, edit backend/.env and add it

# Run
uvicorn main:app --reload
# API at http://127.0.0.1:8000  |  Docs at http://127.0.0.1:8000/docs
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
# App at http://localhost:5173
```

---

## ☁️ Free Online Deployment

| Layer     | Platform       | Free Tier                    |
|-----------|----------------|------------------------------|
| Database  | **Aiven.io**   | Free MySQL, 1 month trial → then use FreeSQLDatabase.com |
| Backend   | **Render.com** | Free FastAPI hosting         |
| Frontend  | **Vercel.com** | Free React/Vite hosting      |

### Best Free MySQL Options Online

| Service | Free Tier | How to get URL |
|---|---|---|
| **FreeSQLDatabase.com** | Free MySQL forever, 5MB | Sign up → instant credentials |
| **Aiven.io** | 1 month free trial | New service → MySQL → copy URI |
| **Railway.app** | $5 free credit/month | New project → MySQL → connect |
| **PlanetScale** | Free hobby tier | New database → connect → copy URL |

### Environment Variables for Production

**Render (backend):**
```
DATABASE_URL = mysql+pymysql://user:pass@host:port/dbname?ssl-mode=REQUIRED
ALLOWED_ORIGINS = https://your-app.vercel.app
```

**Vercel (frontend):**
```
VITE_API_URL = https://your-api.onrender.com
```

See `DEPLOYMENT_GUIDE.html` for full step-by-step instructions.
