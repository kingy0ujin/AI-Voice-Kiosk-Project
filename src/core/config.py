import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    # Add other configuration variables here
    DB_PATH = os.getenv("DB_PATH", "data/menu.db")
    CHROMA_PATH = os.getenv("CHROMA_PATH", "data/chroma")

settings = Settings()
