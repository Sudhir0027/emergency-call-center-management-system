from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from ..models import EmergencyCall, CallHistory, Responder

VALID_TRANSITIONS = {
    "WAITING": {"ASSIGNED", "CANCELLED"},
    "ASSIGNED": {"IN_PROGRESS", "CANCELLED"},
    "IN_PROGRESS": {"RESOLVED", "CANCELLED"},
    "RESOLVED": set(),
    "CANCELLED": set(),
}

def utcnow():
    return datetime.now(timezone.utc)

def record_status(db, call, old_status, new_status, username):
    db.add(CallHistory(call_id=call.call_id, old_status=old_status, new_status=new_status, changed_by=username))

def change_status(db: Session, call: EmergencyCall, new_status: str, username: str):
    old = call.status
    if new_status == old:
        return call
    if new_status not in VALID_TRANSITIONS.get(old, set()):
        raise HTTPException(400, {"success": False, "message": f"Cannot change status from {old} to {new_status}"})
    if new_status == "RESOLVED" and call.assigned_responder_id:
        responder = db.get(Responder, call.assigned_responder_id)
        if responder:
            responder.availability = "AVAILABLE"
    call.status = new_status
    call.updated_at = utcnow()
    record_status(db, call, old, new_status, username)
    return call

def assign_responder(db: Session, call: EmergencyCall, responder_id: int, username: str):
    if call.status not in ("WAITING", "ASSIGNED"):
        raise HTTPException(400, {"success": False, "message": "Only waiting or assigned calls can be assigned"})
    responder = db.get(Responder, responder_id)
    if not responder:
        raise HTTPException(404, {"success": False, "message": "Responder not found"})
    if responder.availability != "AVAILABLE":
        raise HTTPException(400, {"success": False, "message": "Responder is not available"})
    if call.assigned_responder_id and call.assigned_responder_id != responder_id:
        old = db.get(Responder, call.assigned_responder_id)
        if old:
            old.availability = "AVAILABLE"
    responder.availability = "BUSY"
    old_status = call.status
    call.assigned_responder_id = responder_id
    call.status = "ASSIGNED"
    call.updated_at = utcnow()
    if old_status != "ASSIGNED":
        record_status(db, call, old_status, "ASSIGNED", username)
    return call
