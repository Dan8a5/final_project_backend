from fastapi import APIRouter, HTTPException, Depends, Header
from app.models.itinerary import Itinerary
from app.services.openai_service import OpenAIService
from app.utils import get_park_data, get_weather_data
from app.models.itinerary_request import UserPreferences
from app.config.config import supabase_client
from app.dependencies import get_current_user
from datetime import datetime

itineraries_router = APIRouter(prefix="/itineraries", tags=["itineraries"])
openai_service = OpenAIService()

@itineraries_router.get("/user", response_model=list[Itinerary])
async def get_user_itineraries(
    current_user: str = Depends(get_current_user),
    authorization: str = Header(None)
):
    try:
        if authorization and authorization.startswith('Bearer '):
            token = authorization.split(' ')[1]
            supabase_client.auth.set_session(token)
            
        response = supabase_client.table("itineraries").select("*").eq("user_id", current_user).execute()
        
        if response.error:
            raise HTTPException(status_code=400, detail=str(response.error))
            
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
        
        user_id = current_user
        park_data = get_park_data(user_preferences.parkcode)
        print(f"\nPark data retrieved: {park_data}")
        
        weather_data = get_weather_data(park_data["location"])
        print(f"\nWeather data retrieved: {weather_data}")
        
        itinerary_text = await openai_service.generate_itinerary(
            park_data['name'],
            user_preferences.dict(), 
            weather_data
        )
        print(f"\nGenerated itinerary:\n{itinerary_text}")
        
        itinerary_data = {
            "user_id": user_id,
            "title": f"Itinerary for {park_data['name']}",
            "description": itinerary_text,
            "start_date": user_preferences.start_date.isoformat(),
            "end_date": user_preferences.end_date.isoformat(),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        print(f"\nPrepared itinerary data: {itinerary_data}")
        
        response = supabase_client.table("itineraries").insert(itinerary_data).execute()
        print(f"\nDatabase response: {response.data}")
        
        return response.data[0]
        
    except Exception as e:
        print(f"Operation failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@itineraries_router.put("/{itinerary_id}", response_model=Itinerary)
async def update_itinerary(
    itinerary_id: int,
    updated_data: dict,
    current_user: str = Depends(get_current_user),
    authorization: str = Header(None)
):
    try:
        if authorization and authorization.startswith('Bearer '):
            token = authorization.split(' ')[1]
            supabase_client.auth.set_session(token)
            
        existing = supabase_client.table("itineraries").select("user_id").eq("id", itinerary_id).execute()
            
        if not existing.data or existing.data[0]["user_id"] != current_user:
            raise HTTPException(status_code=404, detail="Itinerary not found")
        
        updated_data["updated_at"] = datetime.utcnow().isoformat()
        
        response = supabase_client.table("itineraries").update(updated_data).eq("id", itinerary_id).execute()
            
        if response.error:
            raise HTTPException(status_code=400, detail=str(response.error))
            
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@itineraries_router.delete("/{itinerary_id}")
async def delete_itinerary(
    itinerary_id: int,
    current_user: str = Depends(get_current_user),
    authorization: str = Header(None)
):
    try:
        if authorization and authorization.startswith('Bearer '):
            token = authorization.split(' ')[1]
            supabase_client.auth.set_session(token)
            
        existing = supabase_client.table("itineraries").select("user_id").eq("id", itinerary_id).execute()
            
        if not existing.data or existing.data[0]["user_id"] != current_user:
            raise HTTPException(status_code=404, detail="Itinerary not found")
        
        response = supabase_client.table("itineraries").delete().eq("id", itinerary_id).execute()
            
        if response.error:
            raise HTTPException(status_code=400, detail=str(response.error))
            
        return {"message": "Itinerary deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
