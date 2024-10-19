import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# OpenAI model configuration
OPENAI_MODEL = "gpt-3.5-turbo"

# Typing simulation delay (in seconds)
TYPING_DELAY = 0.05