from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional 
from uuid import UUID
from typing import List


class TripsResponse(BaseModel): 
  id: UUID
  countries: List[str]
  cities: List[str] | None=None

  class Config: 
    from_attributes=True

class TripsCreate(BaseModel): 
  countries: List[str]
  cities: List[str] | None = None
  cities: List[str]

