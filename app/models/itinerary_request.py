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

# Removed ItineraryRequest class since we're getting user_id from token

{
    "parkcode": "yose",
    "num_days": 4,
    "fitness_level": "moderate",
    "preferred_activities": ["hiking", "sightseeing", "photography"],
    "visit_season": "spring",
    "start_date": "2024-04-01",
    "end_date": "2024-04-04"
}
