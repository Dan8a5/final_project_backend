from openai import AsyncOpenAI
from typing import Dict, Optional
from fastapi import HTTPException
from dotenv import load_dotenv
import os

class OpenAIService:
    def __init__(self):
        try:
            load_dotenv()
            self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        except Exception as e:
            raise Exception(f"Failed to initialize OpenAI client: {str(e)}")

    async def generate_park_description(self, park_data: dict) -> str:
        """Generate enhanced park description using GPT-4."""
        try:
            prompt = f"""
            Create an engaging description for {park_data['name']}.
            Include the following sections:

            OVERVIEW
            [Brief introduction and significance]

            MAIN ATTRACTIONS
            [Key features and must-see spots]

            ACTIVITIES
            [Available activities by season]

            VISITOR TIPS
            [Practical advice for visitors]

            Base your response on this park data:
            {park_data}
            """

            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a knowledgeable national park guide providing informative and engaging park descriptions."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error generating description: {str(e)}"
            )

    async def generate_itinerary(self, park_name: str, preferences: dict, weather_data: dict) -> str:
        """Generate a custom itinerary based on preferences and weather."""
        try:
            weather_info = f"Current conditions: {weather_data['current']['conditions']}, {weather_data['current']['temp']}°F"

            prompt = f"""Create a {preferences['num_days']}-day itinerary for {park_name} with:
            Weather: {weather_info}
            Fitness Level: {preferences.get('fitness_level', 'moderate')}
            Activities: {', '.join(preferences.get('preferred_activities', []))}
            Season: {preferences.get('visit_season', 'summer')}

            Include weather-appropriate activities and alternatives based on conditions."""

            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a national parks travel expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error generating itinerary: {str(e)}"
            )

    async def generate_activity_recommendations(self, park_data: dict, season: str) -> str:
        """Generate season-specific activity recommendations."""
        try:
            prompt = f"""
            Create activity recommendations for {park_data['name']} during {season}.
            Include:
            - Best activities for the season
            - Safety considerations
            - Required gear/equipment
            - Timing recommendations

            Base recommendations on this park data:
            {park_data}
            """

            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert park ranger providing seasonal activity recommendations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=400
            )
            return response.choices[0].message.content

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error generating activity recommendations: {str(e)}"
            )
