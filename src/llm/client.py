from src.core.config import settings
import openai

class LLMClient:
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate_response(self, prompt: str, system_role: str = "You are a helpful kiosk assistant.") -> str:
        if not settings.OPENAI_API_KEY:
             return f"LLM Mock Response for: {prompt}"

        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o", # Or gpt-3.5-turbo if 4o not available
                messages=[
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM Error: {e}")
            return "죄송합니다. 서비스에 문제가 발생했습니다."
