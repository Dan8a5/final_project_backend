from sqlmodel import SQLModel, Field
from typing import Dict, Optional
from datetime import datetime
from sqlalchemy import Column, JSON
from uuid import UUID

class Park(SQLModel, table=True):
    __tablename__ = "parks"
    
    id: UUID = Field(primary_key=True)
    parkcode: str = Field(index=True)
    name: str
    description: str
    location: Dict = Field(sa_column=Column(JSON))
    created_at: datetime
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    official_website: str

    class Config:
        arbitrary_types_allowed = True