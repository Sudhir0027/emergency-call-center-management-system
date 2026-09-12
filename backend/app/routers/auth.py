from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserOut, LoginRequest, Token
from ..utils.security import hash_password, verify_password, create_access_token
from ..utils.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserOut, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter((User.username == data.username) | (User.email == data.email)).first():
        raise HTTPException(400, {"success": False, "message": "Username or email already exists"})
    user = User(username=data.username, email=data.email, password_hash=hash_password(data.password), role=data.role.value)
    db.add(user); db.commit(); db.refresh(user)
    return user

@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter((User.username == data.username) | (User.email == data.username)).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, {"success": False, "message": "Invalid username/email or password"})
    return {"access_token": create_access_token({"sub": user.username, "role": user.role}), "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def me(user=Depends(get_current_user)):
    return user
