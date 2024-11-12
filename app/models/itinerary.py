# app/models/itinerary.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, date

class ItineraryPark(SQLModel, table=True):
    __tablename__ = "itinerary_parks"
    
    itinerary_id: int = Field(foreign_key="itinerary.id", primary_key=True)
    park_id: str = Field(foreign_key="parks.id", primary_key=True)
    day_number: int
    notes: Optional[str] = None

class Itinerary(SQLModel, table=True):
    __tablename__ = "itinerary"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str
    start_date: date
    end_date: date
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)