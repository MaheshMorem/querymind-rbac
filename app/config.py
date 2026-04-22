# app/config.py
import os
from dotenv import load_dotenv

# Load variables from .env into os.environ
load_dotenv()

MODE = os.getenv("MODE", "single")  # single | parallel
PROVIDER = os.getenv("PROVIDER", "openai")  # openai | gemini

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Optional: Add a check to catch the error early
if PROVIDER == "openai" and not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment or .env file")
