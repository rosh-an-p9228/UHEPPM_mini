import os
from typing import Optional
from dotenv import load_dotenv

# Load local .env file if available
load_dotenv()

try:
    from pydantic_settings import BaseSettings
    class Settings(BaseSettings):
        APP_NAME: str = "UrbanHeat AI - Climate Intelligence Platform"
        APP_VERSION: str = "2.0.0"
        DEBUG: bool = True
        SECRET_KEY: str = "urbanheat-ai-super-secret-climate-key-2026"
        ALGORITHM: str = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
        DATABASE_URL: str = "sqlite:///./urban_heat.db"
        
        # OpenAI ChatGPT Credentials
        OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
        OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        # Google Maps Platform Credentials
        GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY", "")
        GOOGLE_WEATHER_API_KEY: str = os.getenv("GOOGLE_WEATHER_API_KEY", "")
        GOOGLE_PLACES_API_KEY: str = os.getenv("GOOGLE_PLACES_API_KEY", "")
        GOOGLE_EARTH_ENGINE_PROJECT: str = os.getenv("GOOGLE_EARTH_ENGINE_PROJECT", "")

        # Sensor & Telemetry API Keys
        OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
        TOMTOM_API_KEY: str = os.getenv("TOMTOM_API_KEY", "")
        OPENAQ_API_KEY: str = os.getenv("OPENAQ_API_KEY", "")
        GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
        
        DEFAULT_LAT: float = 19.0330
        DEFAULT_LON: float = 73.0297
        DEFAULT_LOCATION_NAME: str = "Nerul, Navi Mumbai"

        class Config:
            env_file = ".env"
            extra = "allow"
except Exception:
    from pydantic import BaseModel
    class Settings(BaseModel):
        APP_NAME: str = os.getenv("APP_NAME", "UrbanHeat AI - Climate Intelligence Platform")
        APP_VERSION: str = "2.0.0"
        DEBUG: bool = True
        SECRET_KEY: str = os.getenv("SECRET_KEY", "urbanheat-ai-super-secret-climate-key-2026")
        ALGORITHM: str = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
        DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./urban_heat.db")
        
        OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
        OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY", "")
        GOOGLE_WEATHER_API_KEY: str = os.getenv("GOOGLE_WEATHER_API_KEY", "")
        GOOGLE_PLACES_API_KEY: str = os.getenv("GOOGLE_PLACES_API_KEY", "")
        GOOGLE_EARTH_ENGINE_PROJECT: str = os.getenv("GOOGLE_EARTH_ENGINE_PROJECT", "")

        OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
        TOMTOM_API_KEY: str = os.getenv("TOMTOM_API_KEY", "")
        OPENAQ_API_KEY: str = os.getenv("OPENAQ_API_KEY", "")
        GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
        
        DEFAULT_LAT: float = float(os.getenv("DEFAULT_LAT", "19.0330"))
        DEFAULT_LON: float = float(os.getenv("DEFAULT_LON", "73.0297"))
        DEFAULT_LOCATION_NAME: str = os.getenv("DEFAULT_LOCATION_NAME", "Nerul, Navi Mumbai")

settings = Settings()
