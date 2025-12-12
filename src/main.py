from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.core.config import settings
from src.llm.client import LLMClient

from src.rag.vector_db import VectorDB

app = FastAPI(title="AI Voice Kiosk")
llm_client = LLMClient()
vector_db = VectorDB()

# Static files for Kiosk UI
app.mount("/static", StaticFiles(directory="src/static"), name="static")

class ChatRequest(BaseModel):
    text: str
    cart: list = [] # Receive current cart state

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    print(f"User Input: {request.text}, Cart Context: {request.cart}")
    try:
        # 1. RAG: Retrieve relevant menu info based on user input
        rag_context = vector_db.query(request.text, n_results=5)
        
        # Convert cart list to readable string for LLM
        cart_summary = ", ".join([f"{item['name']}" for item in request.cart]) if request.cart else "(비어있음)"

        # System prompt with RAG Context
        system_role = (
            "당신은 스마트한 패스트푸드 키오스크 직원입니다. "
            "손님의 주문이나 요청을 처리하고, 화면의 장바구니를 제어하는 명령어를 출력해야 합니다. "
            f"현재 장바구니 상태: [{cart_summary}] \n"
            "**전체 메뉴 목록 (참고용)**:\n"
            "- 버거: 불고기 버거(5000), 치즈 버거(5500), 새우 버거(6000), 리얼 치즈 버거(7000), 베이컨 버거(6500)\n"
            "- 사이드: 감자튀김(2000), 양파링(2500), 치즈스틱(2000)\n"
            "- 음료: 콜라/사이다(1500), 오렌지 주스(2500), 레모네이드(3000)\n\n"
            "**검색된 상세 정보 (RAG)**:\n"
            f"{rag_context}\n"
            "**규칙**:\n"
            "1. 손님이 메뉴를 **추가**하려 하면 응답 어딘가에 `[ADD: 메뉴명]` 을 포함하세요. (예: `[ADD: 불고기 버거]`)\n"
            "2. 손님이 메뉴를 **취소/삭제**하려 하면 응답 어딘가에 `[REMOVE: 메뉴명]` 을 포함하세요. (예: `[REMOVE: 콜라]`)\n"
            "3. 모든 주문을 취소하면 `[CLEAR]`를 포함하세요.\n"
            "4. 추가 주문 없이 주문을 **완료/결제**하려 하면 맨 마지막에 `[ORDER_COMPLETE]`를 붙이세요.\n"
            "5. 답변은 한국어로 짧고 자연스럽게 하되, 명령어 태그는 정확히 지키세요.\n"
             "6. 질문과 관련 없어 보이는 메뉴라도 위 RAG 정보에 있다면 참고해서 답변하세요.\n"
             "7. 없는 메뉴라고 거짓말하지 마세요. 위 전체 메뉴 목록을 꼭 확인하세요.\n"
        )
        
        response_text = await llm_client.generate_response(request.text, system_role)
        
        # Parse commands from LLM response
        commands = []
        if "[CLEAR]" in response_text:
            commands.append({"type": "clear"})
            response_text = response_text.replace("[CLEAR]", "")

        import re
        # Find ADD commands
        add_matches = re.findall(r'\[ADD:\s*(.*?)\]', response_text)
        for item in add_matches:
            commands.append({"type": "add", "item": item.strip()})
            response_text = response_text.replace(f"[ADD: {item}]", "") # Remove tag from spoken text
            response_text = response_text.replace(f"[ADD:{item}]", "")

        # Find REMOVE commands
        remove_matches = re.findall(r'\[REMOVE:\s*(.*?)\]', response_text)
        for item in remove_matches:
            commands.append({"type": "remove", "item": item.strip()})
            response_text = response_text.replace(f"[REMOVE: {item}]", "")
            response_text = response_text.replace(f"[REMOVE:{item}]", "")

        # Check for order completion tag
        order_complete = False
        if "[ORDER_COMPLETE]" in response_text:
            order_complete = True
            response_text = response_text.replace("[ORDER_COMPLETE]", "").strip()

        return {
            "status": "success", 
            "response": response_text.strip(),
            "order_complete": order_complete,
            "commands": commands
        }
    except Exception as e:
        print(f"Chat Error: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/")
async def root():
    from fastapi.responses import FileResponse
    return FileResponse("src/static/index.html")

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
