# Couple Quiz App

Monorepo untuk aplikasi Couple Quiz dengan backend FastAPI dan frontend Vue 3.

## Quick Start (Dev)
### 1) Backend
```bash
cd backend
python -m venv .venv
```

Aktifkan venv:
```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

Install dependency minimal:
```bash
pip install fastapi uvicorn sqlalchemy openpyxl
```

Jalankan server:
```bash
uvicorn main:app --reload
```

Backend berjalan di `http://localhost:8000`.

### 2) Frontend (Bun)
```bash
cd frontend
bun install
bun run dev
```

Frontend berjalan di `http://localhost:5173` (default Vite).

## Ringkasan Backend
- Framework: FastAPI + SQLAlchemy
- Database: SQLite, file `backend/quiz_booth_a.db` dibuat saat pertama kali jalan
- Endpoint utama:
  - `POST /couple-sessions`
  - `GET /couple-sessions/{id}/questions?player=male|female`
  - `POST /couple-sessions/{id}/submit`
  - `GET /couple-sessions/{id}`
  - `GET /reports/couple-results.xlsx` (download report Excel)
- Status sesi: `created` -> `male_done` -> `done`

## Ringkasan Frontend
- Vue 3 + Vite + Vue Router
- Base URL backend di-hardcode ke `http://localhost:8000`
- Rute utama ada di `frontend/src/router/index.js`

## Struktur Repo
- `backend/` API dan database
- `frontend/` UI aplikasi
