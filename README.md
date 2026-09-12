# Emergency Call Center Management System

Complete React + Tailwind + FastAPI + SQLite college project.

## Run
Backend:
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

Demo accounts:
- admin / Admin@123
- operator / Operator@123

Swagger: `http://localhost:8000/swagger`

Priority queue:
`priority DESC`, then `call_id ASC`.

Example:
102 → 103 → 105 → 101 → 104
