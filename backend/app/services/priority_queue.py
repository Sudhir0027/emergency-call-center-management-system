from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from ..models import EmergencyCall

WAITING_STATUSES = ["WAITING"]

def get_priority_queue(db: Session):
    # Core algorithm: priority DESC, then Call ID ASC.
    return (
        db.query(EmergencyCall)
        .filter(EmergencyCall.status == "WAITING")
        .order_by(desc(EmergencyCall.priority), asc(EmergencyCall.call_id))
        .all()
    )

def get_next_call(db: Session):
    return (
        db.query(EmergencyCall)
        .filter(EmergencyCall.status == "WAITING")
        .order_by(desc(EmergencyCall.priority), asc(EmergencyCall.call_id))
        .first()
    )
