# AI-Powered Code Review System — Local Setup Guide

## What This Project Does

Upload a Python file → get a full code review with:
- **Pylint** — code quality issues
- **Bandit** — security vulnerabilities
- **CodeT5 AI** — smart suggestions powered by the Salesforce CodeT5+ model

---

## One-Click Start (Recommended)

> **Just double-click `setup_and_run.bat`** from the project root.

It will automatically:
1. Check if Python and Node.js are installed
2. Create a Python virtual environment
3. Install all Python dependencies
4. Install all frontend (Node.js) dependencies
5. Start the backend server (port 8000)
6. Start the frontend server (port 5173)
7. Open your browser automatically

---

## Prerequisites (Install These First)

You need two tools installed before running the `.bat` file.

### 1. Python 3.10 or later

Download from: https://www.python.org/downloads/

> **IMPORTANT during install:**
> Check the box that says **"Add Python to PATH"** before clicking Install.

Verify after install by opening Command Prompt and typing:
```
python --version
```

### 2. Node.js 18 or later

Download from: https://nodejs.org/en/download

Choose the **LTS (Long Term Support)** version.

Verify after install:
```
node --version
npm --version
```

---

## Manual Step-by-Step (If bat file doesn't work)

Open **Command Prompt** or **PowerShell** in the project root folder.

### Step 1 — Create Python virtual environment

```cmd
python -m venv venv
```

### Step 2 — Activate the virtual environment

```cmd
venv\Scripts\activate
```

You will see `(venv)` appear at the start of your terminal line.

### Step 3 — Install Python packages

```cmd
pip install -r requirements.txt
```

> This installs FastAPI, PyTorch, Transformers, Pylint, Bandit, and all other dependencies.
> First time will take 5–15 minutes depending on your internet speed.

### Step 4 — Start the backend server

```cmd
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Leave this window open. You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

> **Note:** The very first time, it will also download the **CodeT5+ AI model (~900MB)** from HuggingFace.
> Wait until you see `CodeT5 loaded!` before uploading files.

### Step 5 — Install and start the frontend (new terminal window)

Open a **second** Command Prompt window in the project root:

```cmd
cd frontend
npm install
npm run dev
```

You should see:
```
  VITE v7.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

### Step 6 — Open the app

Open your browser and go to:

- **Frontend UI**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs

---

## Project Structure

```
ai-code-review-system/
├── setup_and_run.bat          ← One-click launcher (Windows)
├── LOCAL_SETUP_GUIDE.md       ← This file
├── requirements.txt           ← Python dependencies
├── docker-compose.yml         ← Docker alternative
│
├── backend/
│   └── app/
│       ├── main.py            ← FastAPI entry point
│       ├── api/v1/endpoints/
│       │   └── review.py      ← /api/v1/review/upload endpoint
│       ├── ai_review/
│       │   └── real_codet5.py ← CodeT5 AI model integration
│       ├── static_analyzers/
│       │   ├── pylint_analyzer.py
│       │   └── bandit_analyzer.py
│       └── core/
│           └── cors.py        ← CORS config for frontend
│
├── frontend/
│   ├── package.json
│   └── src/
│       ├── App.tsx            ← Main React app
│       └── main.tsx
│
└── data/
    └── uploads/               ← Uploaded files stored here
```

---

## API Reference

### POST `/api/v1/review/upload`

Upload a Python file for review.

**Request:** `multipart/form-data` with field `file`

**Response:**
```json
{
  "review_id": "uuid",
  "total_issues": 5,
  "summary": {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 1,
    "info": 1
  },
  "issues": [...]
}
```

### GET `/api/health`

Check if backend is running.

```json
{ "status": "healthy", "message": "FastAPI backend is up!" }
```

---

## How to Stop

- Close the **Backend window** (the one showing uvicorn logs)
- Close the **Frontend window** (the one showing Vite logs)

---

## Troubleshooting

| Problem | Solution |
|--------|---------|
| `python` not recognized | Reinstall Python and check **"Add to PATH"** |
| `npm` not recognized | Reinstall Node.js and restart terminal |
| Backend fails to start | Make sure venv is activated: `venv\Scripts\activate` |
| Port already in use | Kill the process using that port or change the port number |
| Model download stuck | Check your internet connection; the CodeT5 model is ~900MB |
| CORS error in browser | Make sure backend is running on port 8000 |
| `pip install` fails on torch | Try: `pip install torch --index-url https://download.pytorch.org/whl/cpu` |

---

## Running with Docker (Alternative)

If you have Docker Desktop installed:

```cmd
docker-compose up --build
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19, TypeScript, Vite, TailwindCSS |
| Backend | FastAPI, Python, Uvicorn |
| AI Model | Salesforce CodeT5+ 220M (HuggingFace Transformers) |
| Static Analysis | Pylint, Bandit |
| Containerization | Docker, Docker Compose |
