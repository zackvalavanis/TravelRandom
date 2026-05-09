from app.schemas.users import UserResponse, UserCreate
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID 
from app.utils.auth import hash_password, get_current_user


router = APIRouter()

@router.get('/users', response_model=List[UserResponse])
def get_users(db: Session=Depends(get_db)): 
  users = db.query(User).all()
  return users

@router.get('/users/me')
def get_me(current_user: User = Depends(get_current_user)): 
  return current_user