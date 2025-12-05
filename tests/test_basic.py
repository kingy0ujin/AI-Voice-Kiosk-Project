from fastapi.testclient import TestClient
from src.main import app
from src.core.config import settings
import os

client = TestClient(app)

def test_read_main():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "0.1.0"}

def test_settings_load():
    # Verify that settings are loaded (defaults at least)
    assert settings.DB_PATH is not None

def test_stt_import():
    from src.audio.stt import Transcriber
    t = Transcriber()
    assert t is not None

def test_tts_import():
    from src.audio.tts import Synthesizer
    s = Synthesizer()
    assert s is not None

def test_llm_import():
    from src.llm.client import LLMClient
    l = LLMClient()
    assert l is not None

def test_rag_import():
    # This might fail if chromadb needs persistent storage dir to exist and have permissions
    # But let's try
    from src.rag.vector_db import VectorDB
    # Mocking or just checking import for now to avoid side effects in unit test
    assert VectorDB is not None
