import asyncio
from src.llm.client import LLMClient
from src.core.config import settings

async def main():
    print(f"Testing LLM Client with Base URL: {settings.OLLAMA_BASE_URL}")
    print(f"Model: {settings.LLM_MODEL}")
    
    client = LLMClient()
    prompt = "안녕? 너는 누구니?"
    
    print("-" * 20)
    print(f"Prompt: {prompt}")
    print("Generating response... (make sure Ollama is running)")
    
    try:
        response = await client.generate_response(prompt)
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")
        print("Tip: Check if 'ollama serve' is running and 'ollama pull llama3' was executed.")

if __name__ == "__main__":
    asyncio.run(main())
