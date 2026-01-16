from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
  existing = db.query(User).filter(User.email == data.email).first()
  if existing: 
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email Already Registered")

  user = User(email=data.email, hashed_password=hash_password(data.password))
  db.add(user)
  db.commit()
  db.refresh(user)

  token = create_access_token(subject=str(user.id))
  return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
  user = db.query(User).filter(User.email == data.email).first()

  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

  token = create_access_token(subject=str(user.id))
  return {"access_token": token, "token_type": "bearer"}

