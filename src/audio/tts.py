from src.core.config import settings
from gtts import gTTS
import os

class Synthesizer:
    def __init__(self):
        # Initialize ElevenLabs client if needed
        pass

    async def speak(self, text: str, output_file: str = "output.mp3"):
        """
        Convert text to speech using gTTS (fallback) or ElevenLabs.
        """
        try:
            # Fallback to gTTS for now as it is free and easy
            tts = gTTS(text=text, lang='ko')
            tts.save(output_file)
            return output_file
        except Exception as e:
            print(f"TTS Error: {e}")
            return None
