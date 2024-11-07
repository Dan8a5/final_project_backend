import requests
from typing import Dict, Optional
from fastapi import HTTPException
from app.config.config import settings

class WeatherService:
    def __init__(self):
        self.api_key = settings.WEATHER_API_KEY
        self.base_url = "https://api.weatherapi.com/v1"

    async def get_weather(self, latitude: float, longitude: float) -> Dict:
        """Get weather information for a specific location"""
        try:
            response = requests.get(
                f"{self.base_url}/forecast.json",
                params={
                    "key": self.api_key,
                    "q": f"{latitude},{longitude}",
                    "days": 7
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error fetching weather data: {str(e)}"
            )

    async def get_conditions_advice(self, conditions: str) -> str:
        """Get advice based on weather conditions"""
        condition_advice = {
            "clear": "Perfect weather for outdoor activities!",
            "sunny": "Remember sunscreen and bring plenty of water!",
            "rain": "Bring rain gear and check trail conditions.",
            "snow": "Check road conditions and bring appropriate winter gear.",
            "storm": "Consider indoor activities or postpone outdoor plans.",
            "cloudy": "Good conditions for hiking, but bring layers.",
        }
        return condition_advice.get(
            conditions.lower(), 
            "Check local weather reports for specific advice."
        )