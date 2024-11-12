from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.models.itinerary import Itinerary
from app.services.openai_service import OpenAIService
from app.services.pdf_service import PDFService
from app.utils import get_park_data, get_weather_data
from app.models.itinerary_request import UserPreferences
from app.config.config import supabase_client
from app.dependencies import get_current_user
from datetime import datetime

itineraries_router = APIRouter(prefix="/itineraries", tags=["itineraries"])
openai_service = OpenAIService()
pdf_service = PDFService()

@itineraries_router.get("/{itinerary_id}/pdf")
async def get_itinerary_pdf(
    itinerary_id: int,
    current_user: str = Depends(get_current_user),
    authorization: str = Header(None)
):
    try:
        if authorization and authorization.startswith('Bearer '):
            token = authorization.split(' ')[1]
            supabase_client.postgrest.auth(token)  # Changed from auth.set_session to postgrest.auth
        
        response = supabase_client.table("itineraries").select("*").eq("id", itinerary_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Itinerary not found")
            
        itinerary = response.data[0]
        
        # Verify the user owns this itinerary
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
        print(f"PDF generation error: {str(e)}")  # Add logging for debugging
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
        print(f"\nPark data retrieved: {park_data}")
        
        weather_data = get_weather_data(park_data["location"])
        print(f"\nWeather data retrieved: {weather_data}")
        
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
            supabase_client.auth.set_session(token)
        
        response = supabase_client.table("itineraries").select("*").eq("id", itinerary_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Itinerary not found")
            
        itinerary = response.data[0]
        pdf_buffer = pdf_service.generate_itinerary_pdf(itinerary)
        
        headers = {
            'Content-Disposition': f'attachment; filename="itinerary_{itinerary_id}.pdf"',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        }
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers=headers
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
