# 🧠 Project Context: AI Voice Kiosk

이 문서는 AI Voice Kiosk 프로젝트의 기술적 맥락, 아키텍처 원칙, 코딩 컨벤션을 정의합니다.
AI(Assistant)는 코드를 생성하거나 수정할 때 반드시 이 문서를 기준으로 작업해야 합니다.

## 1. 프로젝트 개요 (Project Overview)

목표: 음성(STT)으로 주문을 받고, RAG를 통해 정확한 메뉴 정보를 검색하여, LLM이 자연스러운 음성(TTS)으로 응답하는 키오스크 시스템 구현.

핵심 가치: 빠른 응답 속도, 정확한 의도 파악, 할루시네이션(거짓 정보) 방지.

## 2. 기술 스택 및 버전 (Tech Stack & Versions)

Language: Python 3.11+

Backend Framework: FastAPI (비동기 처리 필수)

AI Components:

LLM: OpenAI gpt-4o (Main), Claude 3.5 Sonnet (Fallback)

STT: OpenAI Whisper (base or small model for local, API for cloud)

TTS: ElevenLabs (High Quality) or gTTS (Free/Test)

Database:

Vector DB: ChromaDB (메뉴 설명, 특징 임베딩 저장)

Relational DB: SQLite (menu.db - 가격, 재고, 품절 여부 등 정형 데이터)

Environment: .env 파일을 통한 API Key 관리 (절대 코드에 하드코딩 금지)

## 3. 디렉토리 구조 및 역할 (Directory Structure)

코드를 작성하거나 파일을 생성할 때 아래 구조를 엄격히 준수하십시오.

ai-voice-kiosk/
├── src/
│   ├── main.py            # FastAPI 앱 진입점 (Lifespan 관리, 엔드포인트 정의)
│   ├── core/              # 설정(Config), 로깅, 예외 처리
│   ├── audio/             # 오디오 처리 모듈
│   │   ├── stt.py         # Speech-to-Text 클래스 (Transcriber)
│   │   └── tts.py         # Text-to-Speech 클래스 (Synthesizer)
│   ├── llm/               # LLM 통신 모듈
│   │   ├── client.py      # OpenAI/Claude API 클라이언트
│   │   └── prompts.py     # 시스템 프롬프트 및 템플릿 관리
│   ├── rag/               # RAG 파이프라인
│   │   ├── vector_db.py   # ChromaDB 초기화 및 검색 로직
│   │   └── ingestion.py   # 데이터 전처리 및 임베딩 적재 (Admin용)
│   ├── schemas/           # Pydantic 모델 (Request/Response 스키마)
│   └── utils/             # 공통 유틸리티 함수
├── data/                  # 로컬 데이터 저장소 (SQLite, ChromaDB 파일)
├── tests/                 # 단위 테스트 (Pytest)
└── requirements.txt       # 의존성 목록


## 4. 아키텍처 원칙 (Architecture Principles)

### 4.1. 비동기 우선 (Async First)

LLM API 호출, DB 조회, 외부 API 통신은 반드시 async/await를 사용하여 Non-blocking으로 구현해야 합니다.

Bad: requests.get(...)

Good: httpx.AsyncClient, await openai.ChatCompletion.acreate(...)

### 4.2. RAG 워크플로우 (Retrieval-Augmented Generation)

Query Analysis: 사용자의 질문에서 핵심 키워드 추출 (예: "시원한 거", "커피").

Hybrid Search:

Semantic Search (Vector): 메뉴 설명, 맛 표현 검색.

Keyword Search (SQL): 가격, 재고 필터링.

Context Injection: 검색된 상위 3~5개 메뉴 정보를 프롬프트에 주입.

Response: LLM이 Context를 기반으로 친절한 응답 생성.

### 4.3. 예외 처리 및 안정성

API 호출 실패 시 재시도(Retry) 로직을 포함해야 합니다.

STT 인식 실패 시 "죄송합니다, 다시 말씀해 주시겠어요?"와 같은 기본 Fallback 응답을 준비합니다.

5. 코딩 컨벤션 (Coding Conventions)

### 5.1. 스타일 가이드

PEP 8 표준을 준수합니다.

Type Hinting: 모든 함수 인자와 반환값에 타입 힌트를 명시합니다.

# Good
async def get_menu_recommendation(query: str) -> List[MenuSchema]:
    ...


Docstrings: Google Style Docstring을 사용하여 함수와 클래스를 설명합니다.

### 5.2. 변수 및 함수 명명

Variables/Functions: snake_case (예: load_menu_data, user_query)

Classes: PascalCase (예: MenuRecommender, AudioProcessor)

Constants: UPPER_CASE (예: MAX_RETRY_COUNT, DEFAULT_MODEL_NAME)

### 6. 데이터 명세 (Data Specifications)

### 6.1. Menu Schema (SQLite & Vector Meta)

메뉴 데이터는 다음 필드를 반드시 포함해야 합니다.

id (int): 고유 ID

name (str): 메뉴 이름 (예: "아이스 아메리카노")

category (str): 카테고리 (예: "Coffee", "Dessert")

price (int): 가격

description (str): 메뉴 설명 (임베딩 대상)

tags (List[str]): 특징 태그 (예: ["카페인", "시원함", "쓴맛"])

is_sold_out (bool): 품절 여부

### 7. 주의 사항 (Constraints)

응답 속도: STT 종료 후 TTS 시작까지 2초 이내를 목표로 합니다. (스트리밍 방식 고려)

보안: 사용자 음성 데이터는 처리 후 즉시 메모리에서 삭제하며, 서버에 영구 저장하지 않습니다.
