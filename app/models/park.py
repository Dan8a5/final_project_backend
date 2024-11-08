from sqlmodel import SQLModel, Field
from typing import Optional, Dict
from datetime import datetime
from sqlalchemy import Column, JSON
import uuid

class Park(SQLModel, table=True):
    __tablename__ = "parks"
    
    id: str = Field(primary_key=True)  # UUID stored as str
    description: str
    location: Dict = Field(default={}, sa_column=Column(JSON))  # jsonb type in Supabase
    parkcode: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    latitude: float
    longitude: float

    class Config:
        arbitrary_types_allowed = True
