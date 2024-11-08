from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.park import Park
from app.dependencies import get_db

def get_park_data(park_code: str):
    """Retrieve park data based on park code."""
    print(f"Starting park data query for: {park_code}")
    try:
        db = next(get_db())
        park = db.exec(select(Park).where(Park.parkcode == park_code)).first()
        
        if not park:
            print(f"No data found for parkcode: {park_code}")
            raise HTTPException(status_code=404, detail="Park not found")

        # Convert SQLModel object to dict with the exact structure needed
        park_dict = {
            "id": park.id,
            "name": park.name,
            "description": park.description,
            "parkcode": park.parkcode,
            "location": park.location,
            "created_at": park.created_at
        }
        return park_dict

    except Exception as e:
        print(f"Error in get_park_data: {str(e)}")
        raise

def get_weather_data(location: dict):
    """Retrieve weather data based on location."""
    print(f"Processing location data: {location}")
    lat = location.get("lat")
    lon = location.get("lng")
    
    weather_data = {
        "current": {
            "temp": 75,
            "conditions": "Sunny"
        }
    }
    return weather_data
