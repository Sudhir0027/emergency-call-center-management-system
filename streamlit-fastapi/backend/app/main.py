from datetime import datetime, timezone
from threading import Lock

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


app = FastAPI(
    title="Emergency Call Center API",
    description="Simple emergency call intake and queue API.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreateCallRequest(BaseModel):
    caller_name: str = Field(strict=True, min_length=1, max_length=100)
    phone: str = Field(strict=True, min_length=3, max_length=30)
    location: str = Field(strict=True, min_length=1, max_length=200)
    emergency_type: str = Field(strict=True, min_length=1, max_length=50)
    description: str = Field(strict=True, min_length=1, max_length=500)
    priority: int = Field(default=3, ge=1, le=5)


class EmergencyCall(CreateCallRequest):
    call_id: int
    status: str
    created_at: datetime


calls: list[EmergencyCall] = []
calls_lock = Lock()
next_call_id = 1001


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/calls", response_model=list[EmergencyCall])
def list_calls() -> list[EmergencyCall]:
    return sorted(calls, key=lambda call: (-call.priority, call.call_id))


@app.post("/api/calls", response_model=EmergencyCall, status_code=201)
def create_call(request: CreateCallRequest) -> EmergencyCall:
    global next_call_id
    with calls_lock:
        call = EmergencyCall(
            **request.model_dump(),
            call_id=next_call_id,
            status="WAITING",
            created_at=datetime.now(timezone.utc),
        )
        next_call_id += 1
        calls.append(call)
    return call


@app.patch("/api/calls/{call_id}/status", response_model=EmergencyCall)
def update_status(call_id: int, status: str) -> EmergencyCall:
    allowed_statuses = {"WAITING", "IN_PROGRESS", "RESOLVED", "CANCELLED"}
    if status not in allowed_statuses:
        raise HTTPException(400, "Invalid status")
    for call in calls:
        if call.call_id == call_id:
            call.status = status
            return call
    raise HTTPException(404, "Call not found")


@app.get("/api/dashboard")
def dashboard() -> dict[str, int]:
    return {
        "total": len(calls),
        "waiting": sum(call.status == "WAITING" for call in calls),
        "in_progress": sum(call.status == "IN_PROGRESS" for call in calls),
        "resolved": sum(call.status == "RESOLVED" for call in calls),
    }
