import os
from typing import Optional

class Settings:
    """Application settings and configuration"""

    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./products.db")
    DATABASE_FILE: str = "products.db"

    # Website Configuration
    WEBSITE_URL: str = os.getenv("WEBSITE_URL", "https://caviaarmode.com")
    MAX_PRODUCTS_TO_SCRAPE: int = int(os.getenv("MAX_PRODUCTS_TO_SCRAPE", "100"))
    SCRAPING_DELAY: float = float(os.getenv("SCRAPING_DELAY", "1.0"))  # seconds between requests

    # Chat Configuration
    MAX_CONVERSATION_HISTORY: int = int(os.getenv("MAX_CONVERSATION_HISTORY", "10"))
    SYSTEM_PROMPT: str = """You are Rufus, an AI shopping assistant for Caviaar Mode, an e-commerce fashion website. 
    You help customers find the perfect products, answer questions about items, compare options, and provide styling advice.

    Key responsibilities:
    1. Help customers discover products based on their needs
    2. Answer specific product questions using available data
    3. Provide styling and fashion advice
    4. Compare different products when requested
    5. Suggest alternatives and complementary items

    Always be helpful, friendly, and knowledgeable about fashion and the products available.
    If you don't have specific product information, say so honestly and offer to help in other ways.
    """

    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # seconds

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")

    def __init__(self):
        """Validate required settings on initialization"""
        if not self.OPENAI_API_KEY:
            print("⚠️  WARNING: OPENAI_API_KEY not set. Please set this environment variable.")

        if not self.WEBSITE_URL:
            print("⚠️  WARNING: WEBSITE_URL not set. Using default.")

# Create global settings instance
settings = Settings()

# Export commonly used settings
OPENAI_API_KEY = settings.OPENAI_API_KEY
OPENAI_MODEL = settings.OPENAI_MODEL
DATABASE_URL = settings.DATABASE_URL
WEBSITE_URL = settings.WEBSITE_URL
SYSTEM_PROMPT = settings.SYSTEM_PROMPT