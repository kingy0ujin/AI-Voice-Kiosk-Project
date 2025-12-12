import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    LLM_MODEL = os.getenv("LLM_MODEL", "gemma3:12b")

    # Add other configuration variables here
    DB_PATH = os.getenv("DB_PATH", "data/menu.db")
    CHROMA_PATH = os.getenv("CHROMA_PATH", "data/chroma")

settings = Settings()
