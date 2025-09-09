"""Application configuration"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # AI Provider Configuration
    ai_provider: str = "openai"  # Options: "openai" or "anthropic"
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # CORS Configuration
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()