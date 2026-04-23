# FundBridger

An online fundraising platform built with FastAPI + React using BCE (Boundary–Control–Entity) architecture.

---

## 1. Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- pip, npm

---

## 2. Backend Setup

```bash
cd fundbridger/backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp ../.env.example .env
# Edit .env with your DATABASE_URL and SECRET_KEY

# Create the PostgreSQL database
psql -U postgres -c "CREATE DATABASE fundbridger;"

# Start the API server (tables are auto-created on startup)
uvicorn main:app --reload --port 8000
```

API docs available at: http://localhost:8000/docs

---

## 3. Frontend Setup

```bash
cd fundbridger/frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

App available at: http://localhost:5173

---

## 4. Seed Data

```bash
cd fundbridger/seed

# Install seed dependencies (if not already installed globally)
pip install faker passlib bcrypt

# Generate SQL seed file
python seed.py

# Load seed data into PostgreSQL
psql -U postgres -d fundbridger -f seed_data.sql
```

This creates 100 user accounts with randomised data (80% Active, 20% Inactive) across all four roles.

---

## 5. Deployment

### Frontend — Vercel

1. Push the `fundbridger/frontend` directory to a GitHub repo.
2. Import the repo in Vercel.
3. Set build command: `npm run build`, output directory: `dist`.
4. Add environment variable `VITE_API_BASE_URL` pointing to your backend URL.

### Backend — Render

1. Push `fundbridger/backend` to a GitHub repo.
2. Create a new **Web Service** on Render.
3. Set:
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add `DATABASE_URL` environment variable.
5. Create a **PostgreSQL** database on Render and link the connection string.

---

## Architecture

```
fundbridger/
├── backend/
│   ├── boundaries/     ← FastAPI routes (HTTP interface layer)
│   ├── controls/       ← Business logic controllers
│   └── entities/       ← SQLAlchemy ORM models
└── frontend/
    └── src/
        ├── api/        ← API calls mapping to controller methods
        ├── components/ ← Reusable UI components
        └── pages/      ← BCE boundary UI pages
```
