from fastapi import APIRouter, Depends
from app.models.itinerary import Itinerary
from app.dependencies import supabase

itineraries_router = APIRouter()

@itineraries_router.post("/itineraries")
async def create_itinerary(itinerary: Itinerary):
    # Implement logic to create a new itinerary in the database
    pass

@itineraries_router.get("/itineraries")
async def get_itineraries():
    # Implement logic to retrieve itineraries for the authenticated user
    pass
