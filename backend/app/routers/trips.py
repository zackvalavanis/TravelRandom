from app.schemas.trips import TripCreate, TripResponse
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.trips import Trip
from app.models.user import User
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from app.utils.auth import get_current_user

router = APIRouter()

@router.get('/trips', response_model=List[TripResponse])
def get_trips(db: Session = Depends(get_db)):
    trips = db.query(Trip).all()
    return trips


@router.get('/trips/{trip_id}', response_model=TripResponse)
def get_trip(trip_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == current_user.id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@router.post('/trips', response_model=TripResponse)
def create_trip(trip: TripCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_trip = Trip(
        countries=trip.countries,
        cities=trip.cities,
        user_id=current_user.id
    )
    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)
    return new_trip

@router.put('/trips/{trip_id}', response_model=TripResponse)
def update_trip(trip_id: UUID, trip: TripCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing_trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == current_user.id).first()
    if not existing_trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    existing_trip.countries = trip.countries
    existing_trip.cities = trip.cities
    db.commit()
    db.refresh(existing_trip)
    return existing_trip

@router.delete('/trips/{trip_id}')
def delete_trip(trip_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == current_user.id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    db.delete(trip)
    db.commit()
    return {"message": "Trip deleted"}