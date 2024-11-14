from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.responses import StreamingResponse
from app.models.itinerary import Itinerary
from app.services.openai_service import OpenAIService
from app.services.pdf_service import PDFService
from app.utils import get_park_data, get_weather_data
from app.models.itinerary_request import UserPreferences
from app.config.config import supabase_client
from app.dependencies import get_current_user
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

itineraries_router = APIRouter(prefix="/itineraries", tags=["itineraries"])
openai_service = OpenAIService()
pdf_service = PDFService()

# Update the ItineraryCreate model to match the exact data types from frontend
class ItineraryCreate(BaseModel):
    title: str
    description: str
    park_code: str
    start_date: str  # Using str since frontend sends date as string
    end_date: str    # Using str since frontend sends date as string
    fitness_level: str
    preferred_activities: List[str]
    visit_season: str
    trip_details: str  # Changed from dict to str to match frontend textarea input


@itineraries_router.get("/user_itineraries")
async def get_user_itineraries(current_user: str = Depends(get_current_user)):
    try:
        response = supabase_client.table("itineraries").select("*").eq("user_id", current_user).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="No itineraries found")

        return response.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@itineraries_router.post("", response_model=Itinerary)
async def create_itinerary(
    user_preferences: UserPreferences,
    current_user: str = Depends(get_current_user),
    authorization: str = Header(None)
):
    try:
        if authorization and authorization.startswith('Bearer '):
            token = authorization.split(' ')[1]
            supabase_client.postgrest.auth(token)
        
        park_data = get_park_data(user_preferences.parkcode)
        print(f"Park data retrieved: {park_data}")
        
        weather_data = get_weather_data(park_data["location"])
        print(f"Weather data retrieved: {weather_data}")
        
        itinerary_text = await openai_service.generate_detailed_itinerary(
            park_data['name'],
            user_preferences.dict(),
            weather_data
        )

        new_itinerary = {
            "user_id": current_user,
            "title": f"{park_data['name']} Trip",
            "start_date": user_preferences.start_date.isoformat(),
            "end_date": user_preferences.end_date.isoformat(),
            "description": itinerary_text
        }

        response = supabase_client.table("itineraries").insert(new_itinerary).execute()
        
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to create itinerary")
            
        return response.data[0]

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@itineraries_router.get("/{itinerary_id}/pdf")
async def get_itinerary_pdf(
    itinerary_id: int,
    current_user: str = Depends(get_current_user),
    authorization: str = Header(None)
):
    try:
        if authorization and authorization.startswith('Bearer '):
            token = authorization.split(' ')[1]
            supabase_client.postgrest.auth(token)
        
        response = supabase_client.table("itineraries").select("*").eq("id", itinerary_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Itinerary not found")
        
        itinerary = response.data[0]

        if itinerary['user_id'] != current_user:
            raise HTTPException(status_code=403, detail="Not authorized to access this itinerary")
        
        pdf_buffer = pdf_service.generate_itinerary_pdf(itinerary)
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="itinerary_{itinerary_id}.pdf"'
            }
        )
    except Exception as e:
        print(f"PDF generation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@itineraries_router.post("/save_itinerary")
async def save_itinerary(
    itinerary_id: int,
    current_user: str = Depends(get_current_user)
):
    try:
        response = supabase_client.table("itineraries").select("*").eq("id", itinerary_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Itinerary not found")
        
        itinerary = response.data[0]

        if itinerary['user_id'] == current_user:
            raise HTTPException(status_code=400, detail="Itinerary is already saved to your profile")
        
        new_itinerary = {
            "user_id": current_user,
            "title": itinerary['title'],
            "start_date": itinerary['start_date'],
            "end_date": itinerary['end_date'],
            "description": itinerary['description']
        }

        response = supabase_client.table("itineraries").insert(new_itinerary).execute()
        
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to save itinerary")
        
        return {"message": "Itinerary saved to your profile successfully", "itinerary": response.data[0]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@itineraries_router.post("/save_new_itinerary")
async def save_new_itinerary(
    itinerary: ItineraryCreate,
    current_user: str = Depends(get_current_user),
    authorization: str = Header(None)
):
    try:
        # Set authentication token for Supabase client
        if authorization and authorization.startswith('Bearer '):
            token = authorization.split(' ')[1]
            supabase_client.postgrest.auth(token)
        
        new_itinerary = {
            "user_id": current_user,
            "title": itinerary.title,
            "start_date": itinerary.start_date,
            "end_date": itinerary.end_date,
            "description": itinerary.description
        }
        
        response = supabase_client.table("itineraries").insert(new_itinerary).execute()
        
        return {"message": "Itinerary saved successfully", "itinerary": response.data[0]}
    except Exception as e:
        print("Error saving itinerary:", str(e))
        raise HTTPException(status_code=400, detail=str(e))
