from fastapi import FastAPI
from src.core.config import settings

app = FastAPI(title="AI Voice Kiosk")

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
