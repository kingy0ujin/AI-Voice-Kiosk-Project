from src.core.config import settings
import openai

class LLMClient:
    def __init__(self):
        # Ollama와의 통신을 위해 base_url 설정
        self.client = openai.AsyncOpenAI(
            base_url=settings.OLLAMA_BASE_URL,
            api_key="ollama" # Ollama는 API 키가 필요 없지만 클라이언트가 요구하므로 더미 값 설정
        )

    async def generate_response(self, prompt: str, system_role: str = "You are a helpful kiosk assistant.") -> str:
        # Ollama는 API Key 체크가 불필요하지만, 안전을 위해 예외 처리 유지
        try:
            response = await self.client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM Error: {e}")
            return "죄송합니다. 서비스에 문제가 발생했습니다."
