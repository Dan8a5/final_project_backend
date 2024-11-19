from openai import AsyncOpenAI
from typing import Dict, Optional
from fastapi import HTTPException
from dotenv import load_dotenv
import os

class OpenAIService:
    """
    Service class for handling OpenAI API interactions in the National Parks Explorer application.
    Provides methods for generating park descriptions, itineraries, and activity recommendations.
    """
    
    def __init__(self):
        """
        Initialize the OpenAI service with API credentials from environment variables.
        Raises exception if initialization fails.
        """
        try:
            load_dotenv()
            self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        except Exception as e:
            raise Exception(f"Failed to initialize OpenAI client: {str(e)}")

    async def generate_park_description(self, park_data: dict) -> str:
        """
        Generate an enhanced park description using GPT-4.
        
        Args:
            park_data (dict): Dictionary containing park information
            
        Returns:
            str: Generated park description with structured sections
            
        Raises:
            HTTPException: If generation fails
        """
        try:
            # Construct prompt with required sections
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

            # Make API call to OpenAI
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
                temperature=0.7,  # Control randomness in response
                max_tokens=500    # Limit response length
            )
            return response.choices[0].message.content

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error generating description: {str(e)}"
            )

    async def generate_detailed_itinerary(self, park_name: str, preferences: dict, weather_data: dict) -> str:
        """
        Generate a detailed park visit itinerary based on user preferences and weather.
        
        Args:
            park_name (str): Name of the park
            preferences (dict): User preferences including duration, activities, etc.
            weather_data (dict): Current weather conditions
            
        Returns:
            str: Structured daily itinerary
            
        Raises:
            HTTPException: If generation fails
        """
        try:
            # Determine accommodation format based on camping preference
            is_camping = 'camping' in preferences['preferred_activities']
            accommodation_format = "🏨 Recommended Campsite: [Name]" if is_camping else "🏨 Recommended Hotel: [Name] (Rating: 4.4+)"

            # Define system prompt with required formatting
            system_prompt = f"""You are an AI assistant integrated into the National Parks Explorer application.

REQUIRED DAILY FORMAT:
📅 Day [Number]: [Title]

Morning:
• [Activity 1 with trail name and distance if applicable]
• [Activity 2]

Afternoon:
• [Activity 1 with trail name and distance if applicable]
• [Activity 2]

Evening:
• [Activity 1]
• [Activity 2]

{accommodation_format}
🍽️ Recommended Restaurant: [Name] (Rating: 4.4+)

---

Follow this exact format for each day of the itinerary."""

            # Construct user prompt with specific details
            user_prompt = f"""Plan a {preferences['num_days']} day trip to {park_name} for the {preferences['visit_season']}.
            Fitness Level: {preferences['fitness_level']} (adjust trail distances accordingly)
            Preferred Activities: {', '.join(preferences['preferred_activities'])}
            Weather: Current conditions: {weather_data['current']['conditions']}, {weather_data['current']['temp']}°F
            Dates: {preferences['start_date']} to {preferences['end_date']}"""

            # Generate itinerary via OpenAI
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.22,  # Lower temperature for more consistent formatting
                max_tokens=3000
            )
            return response.choices[0].message.content

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error generating detailed itinerary: {str(e)}"
            )

    async def generate_activity_recommendations(self, park_data: dict, season: str) -> str:
        """
        Generate season-specific activity recommendations for a park.
        
        Args:
            park_data (dict): Park information
            season (str): Season for activities (e.g., "summer", "winter")
            
        Returns:
            str: Generated activity recommendations
            
        Raises:
            HTTPException: If generation fails
        """
        try:
            # Construct prompt for seasonal activities
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

            # Generate recommendations via OpenAI
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