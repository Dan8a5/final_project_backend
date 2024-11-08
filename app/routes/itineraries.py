from fastapi import APIRouter, HTTPException
from app.models.itinerary import Itinerary
from app.services.openai_service import OpenAIService
from app.utils import get_park_data, get_weather_data  # Import utility functions
from app.models.itinerary_request import ItineraryRequest
from app.config.config import supabase_client  # Import the Supabase client

from datetime import datetime

itineraries_router = APIRouter()
openai_service = OpenAIService()  # Initialize the OpenAIService

@itineraries_router.post("/itineraries", response_model=Itinerary)
async def create_itinerary(itinerary_request: ItineraryRequest):
    """Create a new itinerary using OpenAI."""
    
    user_id = itinerary_request.user_id
    user_preferences = itinerary_request.user_preferences

    # Retrieve park and weather data based on user preferences using parkcode
    park_data = get_park_data(user_preferences.parkcode)  # Now using parkcode
    weather_data = get_weather_data(park_data["location"])

    # Generate itinerary using OpenAI
    itinerary_text = await openai_service.generate_itinerary(
        park_data['fullName'], 
        user_preferences.dict(), 
        weather_data
    )

    # Prepare the data to save in the database
    itinerary_data = {
        "user_id": user_id,
        "title": f"Itinerary for {park_data['fullName']}",
        "description": itinerary_text,
        "start_date": user_preferences.start_date,
        "end_date": user_preferences.end_date,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }

    # Insert the itinerary into the database using the Supabase client
    response = supabase_client.table("itineraries").insert(itinerary_data).execute()
    
    if response.status_code != 201:
        raise HTTPException(status_code=400, detail="Failed to create itinerary")

    return response.data[0]

# Temporary test endpoint to retrieve park data by park code
@itineraries_router.get("/test-parks")
async def test_parks():
    """Test retrieving park data."""
    response = supabase_client.table("parks").select("*").execute()
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch parks")
    return response.data

@itineraries_router.get("/itineraries/{itinerary_id}", response_model=Itinerary)
async def read_itinerary(itinerary_id: int):
    """Retrieve an itinerary by ID."""
    response = supabase_client.table("itineraries").select("*").eq("id", itinerary_id).execute()
    
    if response.status_code != 200 or not response.data:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    
    return response.data[0]

@itineraries_router.put("/itineraries/{itinerary_id}", response_model=Itinerary)
async def update_itinerary(itinerary_id: int, updated_data: dict):
    """Update an existing itinerary."""
    updated_data["updated_at"] = datetime.utcnow().isoformat()  # Update the timestamp
    
    response = supabase_client.table("itineraries").update(updated_data).eq("id", itinerary_id).execute()
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to update itinerary")
    
    return response.data[0]

@itineraries_router.delete("/itineraries/{itinerary_id}")
async def delete_itinerary(itinerary_id: int):
    """Delete an itinerary."""
    response = supabase_client.table("itineraries").delete().eq("id", itinerary_id).execute()
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to delete itinerary")
    
    return {"message": "Itinerary deleted successfully"}
