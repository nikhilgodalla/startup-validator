# config/settings.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Project configuration"""
    
    # API Keys
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    SERPER_API_KEY = os.getenv('SERPER_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Model Selection (FREE options)
    DEFAULT_LLM = "groq"  # or "openai" if you have credits
    
    # Model configurations - UPDATED FOR 2025
    MODELS = {
        "groq": {
            "fast": "llama-3.1-8b-instant",  # Updated model
            "smart": "llama-3.3-70b-versatile",  # This one still works
            "default": "llama-3.3-70b-versatile"  # Updated default
        },
        "openai": {
            "fast": "gpt-3.5-turbo",
            "smart": "gpt-4",
            "default": "gpt-3.5-turbo"
        }
    }
    
    # Paths
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
    
    # Performance
    MAX_EXECUTION_TIME = 60  # seconds
    MAX_RETRIES = 3
    CACHE_ENABLED = True
    
    # Debug
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    VERBOSE = DEBUG

# Create global config instance
config = Config()