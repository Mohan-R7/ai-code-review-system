# How It Works — AI Code Review System

## Overview

A full-stack web app that analyzes Python files using **static analysis + AI suggestions**.

```
User uploads .py file → Backend analyzes → Returns issues with AI fixes → UI displays results
```

---

## Architecture

```
Frontend (React/Vite :5173)
        ↓  POST /api/v1/review/upload
Backend (FastAPI :8000)
        ↓
  ┌─────────────────────────────────┐
  │  Pylint  │  Bandit  │  CodeT5+  │
  └─────────────────────────────────┘
        ↓
  Merged issues returned as JSON
```

---

## Flow Step by Step

### 1. Frontend — [frontend/src/App.tsx](frontend/src/App.tsx)
- User drags/drops a `.py` file onto the dropzone
- Clicks **"Start AI Review"**
- File is sent as `multipart/form-data` via `axios.post` to `http://localhost:8000/api/v1/review/upload`
- Results are rendered as color-coded severity cards (critical → info)

### 2. Backend Entry — [backend/app/main.py](backend/app/main.py)
- FastAPI app with CORS enabled
- Single route group mounted at `/api/v1/review`
- Health check at `/api/health`

### 3. Review Endpoint — [backend/app/api/v1/endpoints/review.py](backend/app/api/v1/endpoints/review.py)
1. Saves uploaded file to `data/uploads/`
2. Runs **Pylint** → style/error issues
3. Runs **Bandit** → security vulnerability issues
4. Merges all issues, passes to **AI layer**
5. Returns a `ReviewResponse` with a severity summary + full issue list

### 4. Static Analyzers

| Analyzer | Tool | Catches | Source tag |
|----------|------|---------|------------|
| [pylint_analyzer.py](backend/app/static_analyzers/pylint_analyzer.py) | `pylint --output-format=json` | Errors, warnings, style, refactor | `pylint` |
| [bandit_analyzer.py](backend/app/static_analyzers/bandit_analyzer.py) | `bandit -f json` | Security flaws (SQLi, eval, etc.) | `bandit` |

Both run as subprocesses, parse JSON output, and map results to `Issue` schema.

### 5. AI Layer — [backend/app/ai_review/real_codet5.py](backend/app/ai_review/real_codet5.py)
- Loads **Salesforce/codet5p-220m** model once at startup (HuggingFace Transformers)
- For every **medium/high/critical** issue, extracts ±10 lines of context
- Sends a prompt: `"Review this code… Problem: <issue> Suggestion:"`
- Appends the AI suggestion as a new `INFO` severity issue tagged `source: "codet5"`

### 6. Data Schema — [backend/app/schemas/review.py](backend/app/schemas/review.py)
```python
Issue:          id, severity, title, description, file_path, line_start, line_end, suggestion, source
ReviewResponse: review_id, total_issues, summary{critical/high/medium/low/info}, issues[]
```

---

## Running the App

### Local (manual)
```bash
# Backend
cd backend
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install && npm run dev
```

### Docker
```bash
docker-compose up --build
# Backend → http://localhost:8000
# Frontend → http://localhost:5173
```

---

## Tech Stack

| Layer | Tech |
|-------|------|
| Frontend | React + TypeScript + Vite + Tailwind |
| Backend | FastAPI + Python |
| Static Analysis | Pylint, Bandit |
| AI Model | Salesforce CodeT5+ 220m (HuggingFace) |
| Container | Docker + docker-compose |
