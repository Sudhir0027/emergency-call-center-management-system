# Emergency Call Center - Streamlit + FastAPI

This is a simple emergency call center project beside the existing React application. It contains:

- `backend`: FastAPI REST API for registering calls, listing the priority queue, updating statuses, and dashboard counts
- `frontend`: Streamlit user interface for call intake and queue management

## Backend

From `streamlit-fastapi\backend`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`.

- Health check: `http://127.0.0.1:8000/health`
- API documentation: `http://127.0.0.1:8000/docs`

## Frontend

From `streamlit-fastapi\frontend`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The UI runs at `http://localhost:8501`.

If the API uses another URL, set it before starting Streamlit:

```powershell
$env:API_URL = "http://127.0.0.1:8000"
streamlit run streamlit_app.py
```

Calls are stored in memory for this simple starter and are cleared when the API restarts.
