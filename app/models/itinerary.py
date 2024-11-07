from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime

class ItineraryPark(SQLModel, table=True):
    __tablename__ = "itinerary_parks"
    
    itinerary_id: int = Field(foreign_key="itinerary.id", primary_key=True)
    park_id: int = Field(foreign_key="parks.id", primary_key=True)  # Changed from park to parks
    day_number: int
    notes: Optional[str] = None

class Itinerary(SQLModel, table=True):
    __tablename__ = "itinerary"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str
    start_date: datetime
    end_date: datetime
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)