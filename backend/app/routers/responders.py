from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Responder
from ..schemas import ResponderCreate, ResponderOut, ResponderUpdate
from ..utils.auth import get_current_user, require_roles
from ..services.responder_service import delete_responder

router = APIRouter(prefix="/responders", tags=["Responders"])

@router.post("", response_model=ResponderOut, status_code=201)
def create(data: ResponderCreate, db: Session = Depends(get_db), user=Depends(require_roles("ADMIN"))):
    r = Responder(**data.model_dump(), type=data.type.value, availability=data.availability.value)
    db.add(r); db.commit(); db.refresh(r); return r

@router.get("", response_model=list[ResponderOut])
def list_all(availability: str | None = None, type: str | None = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    q = db.query(Responder)
    if availability: q = q.filter(Responder.availability == availability)
    if type: q = q.filter(Responder.type == type)
    return q.order_by(Responder.responder_id).all()

@router.get("/{responder_id}", response_model=ResponderOut)
def get(responder_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    r = db.get(Responder, responder_id)
    if not r: raise HTTPException(404, {"success": False, "message": "Responder not found"})
    return r

@router.put("/{responder_id}", response_model=ResponderOut)
def update(responder_id: int, data: ResponderUpdate, db: Session = Depends(get_db), user=Depends(require_roles("ADMIN"))):
    r = db.get(Responder, responder_id)
    if not r: raise HTTPException(404, {"success": False, "message": "Responder not found"})
    for k,v in data.model_dump(exclude_unset=True).items(): setattr(r, k, v.value if hasattr(v, "value") else v)
    db.commit(); db.refresh(r); return r

@router.delete("/{responder_id}", status_code=204)
def delete(responder_id: int, db: Session = Depends(get_db), user=Depends(require_roles("ADMIN"))):
    delete_responder(db, responder_id)
