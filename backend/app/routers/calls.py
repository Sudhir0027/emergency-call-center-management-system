from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, asc
from typing import Optional
from ..database import get_db
from ..models import EmergencyCall, Responder
from ..schemas import CallCreate, CallOut, CallUpdate, PriorityUpdate, StatusUpdate
from ..utils.auth import get_current_user, require_roles
from ..services.priority_queue import get_priority_queue, get_next_call
from ..services.call_service import assign_responder, change_status, utcnow

router = APIRouter(prefix="/calls", tags=["Emergency Calls", "Priority Queue"])

@router.post("", response_model=CallOut, status_code=201)
def create_call(data: CallCreate, db: Session = Depends(get_db), user=Depends(require_roles("ADMIN", "OPERATOR"))):
    call = EmergencyCall(**data.model_dump(), emergency_type=data.emergency_type.value, status="WAITING")
    db.add(call); db.commit(); db.refresh(call)
    from ..models import CallHistory
    db.add(CallHistory(call_id=call.call_id, old_status=None, new_status="WAITING", changed_by=user.username))
    db.commit(); db.refresh(call)
    return call

@router.get("", response_model=list[CallOut])
def list_calls(
    status: Optional[str] = None,
    emergency_type: Optional[str] = None,
    priority: Optional[int] = Query(None, ge=1, le=5),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    q = db.query(EmergencyCall).options(joinedload(EmergencyCall.responder))
    if status: q = q.filter(EmergencyCall.status == status)
    if emergency_type: q = q.filter(EmergencyCall.emergency_type == emergency_type)
    if priority: q = q.filter(EmergencyCall.priority == priority)
    if search:
        term = f"%{search}%"
        from sqlalchemy import or_
        q = q.filter(or_(EmergencyCall.caller_name.ilike(term), EmergencyCall.caller_phone.ilike(term), EmergencyCall.location.ilike(term), EmergencyCall.call_id.cast(str).ilike(term)))
    return q.order_by(desc(EmergencyCall.created_at)).all()

@router.get("/queue", response_model=list[CallOut])
def queue(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_priority_queue(db)

@router.get("/next", response_model=CallOut)
def next_call(db: Session = Depends(get_db), user=Depends(get_current_user)):
    call = get_next_call(db)
    if not call:
        raise HTTPException(404, {"success": False, "message": "No waiting emergency calls"})
    return call

@router.get("/{call_id}", response_model=CallOut)
def get_call(call_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    call = db.query(EmergencyCall).options(joinedload(EmergencyCall.responder)).filter(EmergencyCall.call_id == call_id).first()
    if not call: raise HTTPException(404, {"success": False, "message": "Call not found"})
    return call

@router.put("/{call_id}", response_model=CallOut)
def update_call(call_id: int, data: CallUpdate, db: Session = Depends(get_db), user=Depends(require_roles("ADMIN", "OPERATOR"))):
    call = db.get(EmergencyCall, call_id)
    if not call: raise HTTPException(404, {"success": False, "message": "Call not found"})
    if call.status in ("RESOLVED", "CANCELLED"):
        raise HTTPException(400, {"success": False, "message": "Completed calls cannot be edited"})
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(call, k, v.value if hasattr(v, "value") else v)
    call.updated_at = utcnow()
    db.commit(); db.refresh(call)
    return call

@router.delete("/{call_id}", status_code=204)
def delete_call(call_id: int, db: Session = Depends(get_db), user=Depends(require_roles("ADMIN"))):
    call = db.get(EmergencyCall, call_id)
    if not call: raise HTTPException(404, {"success": False, "message": "Call not found"})
    db.delete(call); db.commit()

@router.post("/{call_id}/assign", response_model=CallOut)
def assign(call_id: int, responder_id: int, db: Session = Depends(get_db), user=Depends(require_roles("ADMIN", "OPERATOR"))):
    call = db.get(EmergencyCall, call_id)
    if not call: raise HTTPException(404, {"success": False, "message": "Call not found"})
    assign_responder(db, call, responder_id, user.username)
    db.commit(); db.refresh(call)
    return call

@router.put("/{call_id}/status", response_model=CallOut)
def status(call_id: int, data: StatusUpdate, db: Session = Depends(get_db), user=Depends(require_roles("ADMIN", "OPERATOR"))):
    call = db.get(EmergencyCall, call_id)
    if not call: raise HTTPException(404, {"success": False, "message": "Call not found"})
    change_status(db, call, data.status.value, user.username)
    db.commit(); db.refresh(call)
    return call

@router.put("/{call_id}/priority", response_model=CallOut)
def priority(call_id: int, data: PriorityUpdate, db: Session = Depends(get_db), user=Depends(require_roles("ADMIN", "OPERATOR"))):
    call = db.get(EmergencyCall, call_id)
    if not call: raise HTTPException(404, {"success": False, "message": "Call not found"})
    if call.status in ("RESOLVED", "CANCELLED"):
        raise HTTPException(400, {"success": False, "message": "Cannot change priority of a closed call"})
    call.priority = data.priority; call.updated_at = utcnow()
    db.commit(); db.refresh(call)
    return call
