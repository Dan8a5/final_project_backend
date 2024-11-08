# app/utils.py

# app/utils.py

from fastapi import HTTPException
from app.dependencies import supabase  # Ensure this is imported

def get_park_data(park_code: str):
    """Retrieve park data based on park code."""
    response = supabase.table("parks").select("*").eq("parkcode", park_code).execute()

    # Check if the response contains any data
    if not response.data:
        raise HTTPException(status_code=404, detail="Park not found")

    return response.data[0]  # Return the first result



def get_weather_data(location: dict):
    """Retrieve weather data based on location."""
    # This is a placeholder for actual weather data retrieval logic.
    # You may need to call a weather API, for example, OpenWeatherMap API.
    
    # Sample implementation (you'll need to replace this with actual API calls):
    # For the sake of example, let's assume location is a dict with latitude and longitude
    lat = location.get("latitude")
    lon = location.get("longitude")
    
    # Here you would call a weather API to get the data
    # Example using requests (ensure you install requests if using):
    # response = requests.get(f"https://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q={lat},{lon}")

    # Mock response for illustration
    weather_data = {
        "current": {
            "temp": 75,
            "conditions": "Sunny"
        }
    }
    
    # Return mock data for now
    return weather_data
