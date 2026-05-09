from sqlalchemy import Column, String, Integer, Float, DateTime, func
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID 
import uuid


class Trip(Base): 
  __tablename__ = 'trips'
  id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
  countries = Column(ARRAY(String), nullable=False)
  cities = Column(ARRAY(String))
  notes = Column(Text, nullable=True)

  owner = relationship("User", back_populates="trips")

  