from sqlmodel import Session
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client
from app.config.config import settings, engine, SUPABASE_URL, SUPABASE_KEY
from .services.nps_service import NPSService
from .services.openai_service import OpenAIService
from .services.weather_service import WeatherService

# Security
security = HTTPBearer()

# Database dependency
def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()

# Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    try:
        user = supabase.auth.get_user(credentials.credentials)
        return user.user.id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )