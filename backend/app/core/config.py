from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "CondoMate"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "CondoMate API for condominium management"
    API_V1_STR: str = "/api/v1"
    
    # Backend URL
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000")
    
    # MongoDB settings
    MONGO_DB_URL: str = os.getenv("MONGO_DB_URL", "mongodb://localhost:27017")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "condomate")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_HOSTS: List[str] = [
        "http://localhost",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://18.233.58.28",
        "http://18.233.58.28:5174",
        "http://18.233.58.28:5173",
        "https://0s85lrdrl0.execute-api.us-east-1.amazonaws.com",
        "https://0s85lrdrl0.execute-api.us-east-1.amazonaws.com/prod",
        "*"  # Allow all origins during development
    ]
    
    # Server settings
    HOST: str = "0.0.0.0"  # Listen on all interfaces
    PORT: int = 8000
    RELOAD: bool = False
    
    model_config = ConfigDict(case_sensitive=True, env_file=".env")

settings = Settings()
