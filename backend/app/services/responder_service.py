from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import Responder

def delete_responder(db: Session, responder_id: int):
    responder = db.get(Responder, responder_id)
    if not responder:
        raise HTTPException(404, {"success": False, "message": "Responder not found"})
    if responder.availability == "BUSY":
        raise HTTPException(400, {"success": False, "message": "Busy responder cannot be deleted"})
    db.delete(responder)
    db.commit()
