# Project Context & Specifications

## 1. 핵심 파일 구조 (Core File Structure)
이 프로젝트는 **Backend-First** 구조 위에 정적 프론트엔드 파일을 서빙하는 형태를 취하고 있습니다.

```
AI-Voice-Kiosk-Project/
├── src/
│   ├── main.py                # [Entry Point] FastAPI 앱, 라우팅, LLM 엔드포인트 정의
│   ├── core/config.py         # [Config] 환경설정 (Ollama URL, Model ID, DB 경로)
│   ├── llm/client.py          # [AI] Custom OpenAI Client를 이용한 Ollama 통신 래퍼
│   ├── rag/vector_db.py       # [RAG] ChromaDB 초기화, 데이터 삽입, 유사도 검색 로직
│   └── static/                # [Frontend]
│       ├── index.html         # 전체 UI 레이아웃 (Grid/Flex 기반 3단 구성)
│       ├── style.css          # CSS 변수 기반 다크 테마, 애니메이션 스타일
│       └── script.js          # Web Speech API 제어, Fetch 통신, DOM 조작
└── data/                      # [Persistence] ChromaDB 데이터 저장소
```

---

## 2. 데이터 명세 (Data Specifications)

### **2.1. Vector DB Schema (ChromaDB)**
메뉴 데이터는 아래와 같은 메타데이터 구조로 저장되어 RAG 검색에 활용됩니다.
- **Collection Name**: `menu_items`
- **Document (Content)**: 메뉴의 상세 설명 (예: "톡 쏘는 탄산이 버거의 느끼함을...")
- **Metadata**:
  - `name`: 메뉴명 (Unique ID 역할)
  - `price`: 가격 (Integer)
  - `category`: 카테고리 (버거, 사이드, 음료)

### **2.2. API Spec (`/api/chat`)**
프론트엔드와 백엔드 간의 통신 규격입니다.

**Request (JSON)**
```json
{
  "text": "사용자 발화 내용",
  "cart": [
    { "name": "불고기 버거", "price": 5000 },
    { "name": "콜라", "price": 1500 }
  ]
}
```

**Response (JSON)**
```json
{
  "status": "success",
  "response": "네, 불고기 버거 하나 추가해 드렸습니다.",
  "order_complete": false,  // true일 경우 주문 종료 프로세스 실행
  "commands": [             // UI 제어 명령 목록
    { "type": "add", "item": "불고기 버거" }
  ]
}
```

---

## 3. 기술적 제약 사항 (Technical Constraints)

1.  **브라우저 의존성 (Browser Dependency)**:
    - **Web Speech API**를 사용하므로, **Google Chrome** 브라우저가 필수적입니다. 다른 브라우저에서는 음성 인식 품질이 떨어지거나 동작하지 않을 수 있습니다.
    - HTTPS 또는 localhost 환경에서만 마이크 권한 획득이 가능합니다.

2.  **로컬 리소스 요구사항 (Hardware)**:
    - **Ollama (Gemma3:12b)** 모델을 구동하기 위해 최소 8GB 이상의 VRAM(GPU) 또는 16GB 이상의 시스템 RAM이 권장됩니다.
    - 사양이 낮을 경우 응답 속도(Latency)가 느려져 실시간 대화 경험이 저하될 수 있습니다.

3.  **컨텍스트 윈도우 (Context Window)**:
    - 현재 채팅 히스토리 전체를 LLM에 보내는 것이 아니라, **현재 발화 + 장바구니 상태**만 보냅니다. 따라서 "아까 말한 그거 취소해줘" 같은 멀티턴 참조 기능은 제한적일 수 있습니다.

---

## 4. 개선 사항 (Future Improvements)

1.  **멀티턴 대화 메모리 (Conversation Memory)**:
    - LangChain 등을 도입하여 이전 대화 문맥을 유지하면 더 자연스러운 연속 대화가 가능합니다.
    
2.  **데이터베이스 마이그레이션**:
    - 현재 하드코딩된 메뉴 데이터를 SQLite나 PostgreSQL로 이관하여 관리자 페이지에서 메뉴를 수정할 수 있도록 개선이 필요합니다.

3.  **TTS 품질 향상**:
    - 브라우저 기본 TTS 대신, ElevenLabs나 OpenAI TTS API를 연동하면 더욱 사람 같은 목소리를 제공할 수 있습니다.

4.  **동시성 처리**:
    - 여러 키오스크가 동시에 한 서버에 접속할 경우를 대비해 Vector DB 세션 관리 및 LLM 큐잉 시스템 도입이 필요합니다.
