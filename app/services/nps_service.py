import requests
from typing import List, Optional, Dict
from fastapi import HTTPException
from app.config.config import settings

class NPSService:
    def __init__(self):
        self.api_key = settings.NPS_API_KEY
        self.base_url = "https://developer.nps.gov/api/v1"

    async def get_parks(self, state: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """Get list of national parks"""
        try:
            params = {
                "api_key": self.api_key,
                "limit": limit
            }
            if state:
                params["stateCode"] = state

            response = requests.get(
                f"{self.base_url}/parks",
                params=params
            )
            response.raise_for_status()
            return response.json()["data"]
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error fetching parks: {str(e)}"
            )

    async def get_park_details(self, park_code: str) -> Dict:
        """Get detailed information about a specific park"""
        try:
            response = requests.get(
                f"{self.base_url}/parks",
                params={
                    "api_key": self.api_key,
                    "parkCode": park_code
                }
            )
            response.raise_for_status()
            data = response.json()["data"]
            return data[0] if data else None
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error fetching park details: {str(e)}"
            )