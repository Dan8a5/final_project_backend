# app/models/itinerary_request.py
from pydantic import BaseModel
from typing import List

class UserPreferences(BaseModel):
    parkcode: str  # Change this from park_id to parkcode
    num_days: int
    fitness_level: str
    preferred_activities: List[str]
    visit_season: str
    start_date: str
    end_date: str

class ItineraryRequest(BaseModel):
    user_id: str  # Keep as string for UUID
    user_preferences: UserPreferences
