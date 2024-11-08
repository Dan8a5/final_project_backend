import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pathlib import Path
from sqlmodel import SQLModel, create_engine
from supabase import create_client, Client  # Import Supabase client

# Load environment variables first
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
NPS_API_KEY = os.getenv("NPS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")  # Add default empty string

class Settings(BaseSettings):
    DATABASE_URL: str
    API_V1_STR: str = "/api/v1"

    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    NPS_API_KEY: str = os.getenv("NPS_API_KEY")
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "")  # Add to settings class too

    # Auth
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

settings = Settings()

# Create Supabase client
supabase_client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=False  # Set to True if you want to see SQL queries
)

# Database initialization function
def init_db():
    SQLModel.metadata.create_all(bind=engine)
