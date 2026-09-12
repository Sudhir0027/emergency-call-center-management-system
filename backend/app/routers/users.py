from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserOut
from ..utils.auth import require_roles
from ..utils.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=list[UserOut])
def users(db: Session = Depends(get_db), user=Depends(require_roles("ADMIN"))):
    return db.query(User).order_by(User.id).all()

@router.post("", response_model=UserOut, status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db), user=Depends(require_roles("ADMIN"))):
    if db.query(User).filter((User.username == data.username) | (User.email == data.email)).first():
        raise HTTPException(400, {"success": False, "message": "Username or email already exists"})
    u = User(username=data.username, email=data.email, password_hash=hash_password(data.password), role=data.role.value)
    db.add(u); db.commit(); db.refresh(u); return u
