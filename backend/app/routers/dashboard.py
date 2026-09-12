from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from ..database import get_db
from ..models import EmergencyCall, Responder
from ..utils.auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats")
def stats(db: Session = Depends(get_db), user=Depends(get_current_user)):
    def calls(s=None):
        q = db.query(func.count(EmergencyCall.call_id))
        return q.filter(EmergencyCall.status == s).scalar() if s else q.scalar()
    return {
        "total_calls": calls(),
        "waiting_calls": calls("WAITING"),
        "active_calls": db.query(func.count(EmergencyCall.call_id)).filter(EmergencyCall.status.in_(["ASSIGNED","IN_PROGRESS"])).scalar(),
        "resolved_calls": calls("RESOLVED"),
        "critical_emergencies": db.query(func.count(EmergencyCall.call_id)).filter(EmergencyCall.priority == 5, EmergencyCall.status.notin_(["RESOLVED","CANCELLED"])).scalar(),
        "available_responders": db.query(func.count(Responder.responder_id)).filter(Responder.availability == "AVAILABLE").scalar(),
        "busy_responders": db.query(func.count(Responder.responder_id)).filter(Responder.availability == "BUSY").scalar(),
        "offline_responders": db.query(func.count(Responder.responder_id)).filter(Responder.availability == "OFFLINE").scalar(),
    }

@router.get("/recent-calls")
def recent(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(EmergencyCall).order_by(desc(EmergencyCall.created_at)).limit(8).all()

@router.get("/emergency-distribution")
def distribution(db: Session = Depends(get_db), user=Depends(get_current_user)):
    rows = db.query(EmergencyCall.emergency_type, func.count(EmergencyCall.call_id)).group_by(EmergencyCall.emergency_type).all()
    return [{"type": typ, "count": count} for typ, count in rows]
