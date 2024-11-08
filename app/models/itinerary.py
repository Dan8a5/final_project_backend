from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, date

class ItineraryPark(SQLModel, table=True):
    __tablename__ = "itinerary_parks"
    
    itinerary_id: int = Field(foreign_key="itinerary.id", primary_key=True)
    park_id: str = Field(foreign_key="parks.id", primary_key=True)  # Changed to `str` for UUID
    day_number: int
    notes: Optional[str] = None

class Itinerary(SQLModel, table=True):
    __tablename__ = "itinerary"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)  # Keep as `str` for UUID
    title: str
    start_date: date  # Use `date` to match the database field type
    end_date: date    # Use `date` to match the database field type
    description: Optional[str] = None  # Map `notes` to `description`
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
