from app.schemas.users import UserResponse, UserCreate
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.trips import Trip
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID 
from app.utils.auth import hash_password, get_current_user

