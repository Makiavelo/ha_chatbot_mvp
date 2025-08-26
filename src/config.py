import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PHARMACY_API_URL = os.getenv(
    "PHARMACY_API_URL", "https://67e14fb758cc6bf785254550.mockapi.io/pharmacies"
)
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")
