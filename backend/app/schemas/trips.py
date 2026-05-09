from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional 
from uuid import UUID
from typing import List


class TripResponse(BaseModel): 
  id: UUID
  countries: List[str]
  cities: List[str] | None=None
  revealed_country: str | None = None
  share_code: str | None = None
  is_revealed: bool

  class Config: 
    from_attributes=True

class TripCreate(BaseModel): 
  countries: List[str]
  cities: List[str] | None = None

class EncodedTripResponse(BaseModel):
    id: UUID
    share_code: str
    is_revealed: bool

    class Config:
        from_attributes = True