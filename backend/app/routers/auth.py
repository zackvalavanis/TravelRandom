from app.schemas.users import LoginRequest, TokenResponse, UserCreate
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from typing import List 
from fastapi import APIRouter, Depends, HTTPException 
from uuid import UUID
from app.utils.auth import verify_password, create_access_token, hash_password

router = APIRouter()

@router.post('/auth/login', response_model=TokenResponse)
def login(auth: LoginRequest, db: Session=Depends(get_db)): 
  user = db.query(User).filter(User.email == auth.email).first()

  if not user: 
    raise HTTPException(status_code=401, detail="Invalid credentials")
  
  if not verify_password(auth.password, user.hashed_password): 
    raise HTTPException(status_code=401, detail='Invalid credentials')
  
  token = create_access_token({"sub": user.email})
  return {
    "access_token": token,
    "token_type": "bearer"
  }
  
@router.post('/auth/register', response_model=TokenResponse)
def register(auth: UserCreate, db: Session=Depends(get_db)):
  existing_user = db.query(User).filter(User.email == auth.email).first()
  if existing_user:
    raise HTTPException(status_code=400, detail="User already exists")

  hashed_pw = hash_password(auth.password)

  new_user = User (
    email=auth.email, 
    first_name=auth.first_name, 
    last_name=auth.last_name, 
    hashed_password=hashed_pw
  )

  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  token = create_access_token({"sub": new_user.email})

  return {
    "access_token": token, 
    "token_type": "bearer"
  }
    