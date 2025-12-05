from src.core.config import settings
import openai

class Transcriber:
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def transcribe(self, audio_file_path: str) -> str:
        """
        Transcribe audio file to text using OpenAI Whisper API.
        """
        if not settings.OPENAI_API_KEY:
            return "STT Mock: OpenAI API Key not missing."
            
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = await self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            return transcript
        except Exception as e:
            print(f"STT Error: {e}")
            return "죄송합니다. 다시 말씀해 주세요."
