# app/models/itinerary_request.py
from pydantic import BaseModel
from typing import List
from datetime import date

class UserPreferences(BaseModel):
    parkcode: str
    num_days: int
    fitness_level: str
    preferred_activities: List[str]
    visit_season: str
    start_date: date
    end_date: date

class ItineraryRequest(BaseModel):
    user_id: str  # Keep as string for UUID
    user_preferences: UserPreferences
