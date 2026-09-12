# Emergency Call Center Management System

## Overview
A full-stack college project that simulates emergency call intake, priority queue processing, responder assignment, status tracking and analytics.

## Stack
- FastAPI + SQLAlchemy + SQLite
- JWT + bcrypt password hashing
- React + Tailwind CSS + Axios
- React Router + Lucide React
- Pytest

## Priority algorithm
Waiting calls are always sorted by:
`priority DESC, call_id ASC`

Therefore 101=3, 102=5, 103=5, 104=2, 105=4 produces:
`102 → 103 → 105 → 101 → 104`.

The implementation is isolated in `app/services/priority_queue.py`.

## Backend setup
```bash
cd backend
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```
API: http://localhost:8000  
Swagger: http://localhost:8000/swagger  
ReDoc: http://localhost:8000/redoc

## Frontend setup
```bash
cd frontend
npm install
npm run dev
```
UI: http://localhost:5173

## Demo credentials
- Admin: `admin` / `Admin@123`
- Operator: `operator` / `Operator@123`

## Database
SQLite is created automatically as `backend/emergency.db`. SQLAlchemy keeps the model portable to PostgreSQL; set `DATABASE_URL` to a PostgreSQL URL when migrating.

## API
Authentication:
- POST `/api/auth/register`
- POST `/api/auth/login`
- GET `/api/auth/me`

Calls:
- POST/GET `/api/calls`
- GET `/api/calls/{call_id}`
- PUT/DELETE `/api/calls/{call_id}`
- GET `/api/calls/queue`
- GET `/api/calls/next`
- POST `/api/calls/{call_id}/assign?responder_id=1`
- PUT `/api/calls/{call_id}/status`
- PUT `/api/calls/{call_id}/priority`

Responders:
- POST/GET `/api/responders`
- GET/PUT/DELETE `/api/responders/{responder_id}`

Dashboard:
- GET `/api/dashboard/stats`
- GET `/api/dashboard/recent-calls`
- GET `/api/dashboard/emergency-distribution`

## Security
Change `SECRET_KEY` in `.env` before deployment. Never commit `.env`.

## Tests
```bash
cd backend
pytest -q
```

## Future enhancements
WebSockets, GIS mapping, SMS/voice integration, PostgreSQL deployment, audit logs and advanced dispatch optimization.
