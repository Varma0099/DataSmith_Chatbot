import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

# Model Configuration
MODEL_NAME = "gemini-2.5-flash"  # Updated from deprecated gemini-pro
TEMPERATURE = 0.7
MAX_TOKENS = 2048

# App Configuration
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Validate required keys
def validate_config():
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not set in .env file")
    return True