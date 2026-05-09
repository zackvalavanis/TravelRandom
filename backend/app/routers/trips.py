from app.schemas.trips import TripCreate, TripResponse, EncodedTripResponse
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.trip import Trip
from app.models.user import User
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from app.utils.auth import get_current_user
import random
import string

router = APIRouter()


def generate_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


@router.get('/trips', response_model=List[TripResponse])
def get_trips(db: Session = Depends(get_db)):
    trips = db.query(Trip).all()
    return trips

@router.get('/trips/randomize', response_model=EncodedTripResponse)
def randomize_trip(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    trips = db.query(Trip).filter(Trip.user_id == current_user.id).all()
    if not trips:
        raise HTTPException(status_code=404, detail="No trips found")
    winner = random.choice(trips)
    return winner

@router.post('/trips/encode', response_model=EncodedTripResponse)
def encode_trip(trip: TripCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    code = generate_code()
    winner = random.choice(trip.countries)
    
    new_trip = Trip(
        countries=trip.countries,       # all options
        revealed_country=winner,        # the random pick
        user_id=current_user.id,
        share_code=code,
        is_revealed=False
    )
    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)
    return new_trip


@router.get('/trips/decode/{share_code}', response_model=TripResponse)
def decode_trip(share_code: str, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.share_code == share_code).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Invalid code")
    trip.is_revealed = True
    db.commit()
    db.refresh(trip)
    return trip


@router.get('/trips/{trip_id}', response_model=TripResponse)
def get_trip(trip_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == current_user.id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


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