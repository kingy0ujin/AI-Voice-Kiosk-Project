### 2025학년도 2학기 최신인공지능 미니프로젝트
---
# 🎙️ AI Voice Kiosk Project (LLM 기반 대화형 키오스크)

## 1. 개요 및 목적 (Overview)

"터치보다 편한 대화형 주문 경험"

이 프로젝트는 기존의 터치 기반 키오스크에 **LLM(Large Language Model)**과 RAG(Retrieval-Augmented Generation) 기술을 도입하여, 사용자가 자연어로 대화하며 주문할 수 있는 시스템을 구축하는 것을 목표로 합니다.

단순한 음성 명령(STT)을 넘어, 사용자의 **의도를 파악(NLU)**하고 매장 데이터베이스와 연동하여 **실시간 정보(RAG)**를 제공하며, 이전 대화 맥락을 기억해 **개인화된 추천(Multi-turn)**을 제공합니다.

## 🎯 프로젝트 해결 과제

복잡한 메뉴 탐색 해소: "오늘 점심 뭐 먹지?"와 같은 추상적인 질문에 답변 제공.

동적 정보 처리: 품절, 신메뉴, 알레르기 정보 등을 실시간으로 반영하여 응답.

자연스러운 상호작용: 로봇 같은 단답형이 아닌, 사람과 대화하는 듯한 음성 피드백 제공.

## 2. 시스템 아키텍처 및 워크플로우 (Architecture)

이 프로젝트는 **STT -> RAG/LLM -> TTS**의 파이프라인으로 구성됩니다.

Input (User Voice): 사용자의 음성 입력 (예: "매운 거 말고 딴 거 추천해줘")

STT (Speech-to-Text): 음성을 텍스트로 변환 (Whisper 등 활용)

Orchestrator (Main Logic):

사용자 의도 분석 (주문 vs 정보 탐색)

RAG: ChromaDB/FAISS에서 메뉴, 재고, 이벤트 정보 검색

LLM Generation: 검색된 정보(Context)와 사용자 질문을 결합하여 자연어 응답 생성

TTS (Text-to-Speech): 생성된 텍스트를 음성으로 변환하여 출력

## 3. 기술 스택 (Tech Stack)

AI 개발 도구(IDE) 및 팀원이 환경을 구성할 때 다음 스택을 기준으로 합니다.

구분

기술/라이브러리

버전(권장)

용도

Language

Python

3.11+

전체 프로젝트 메인 언어

LLM

OpenAI API (GPT-4o) / Claude 3.5

Latest

자연어 이해 및 응답 생성

STT

OpenAI Whisper / Google STT

-

고정밀 음성 인식

TTS

gTTS / OpenAI TTS / ElevenLabs

-

자연스러운 음성 출력

Backend

FastAPI

0.100+

비동기 API 처리 및 웹소켓 통신

Vector DB

ChromaDB / FAISS

-

메뉴 데이터 임베딩 및 RAG 검색

Data

SQLite / JSON

-

정형 데이터(가격, 재고) 관리

## 4. 핵심 기능 (Key Features)

1️⃣ 자연어 이해 (NLU) & 의도 파악

단순 키워드 매칭이 아닌 문맥적 의미를 파악합니다.

예시: "이거 말고 더 시원한 거 없어?" → '현재 선택한 메뉴' 제외 + '차가운 음료' 필터링

2️⃣ RAG 기반 지식 베이스 (Knowledge Base)

LLM의 환각(Hallucination)을 방지하고 최신 매장 정보를 반영합니다.

메뉴 DB(이름, 가격, 특징, 알레르기 정보)를 벡터화하여 검색합니다.

3️⃣ 멀티턴(Multi-turn) 대화 관리

대화의 히스토리를 메모리에 저장하여 문맥을 유지합니다.

User: "라떼 줘" -> AI: "따뜻한 걸로 드릴까요?" -> User: "아니 차가운 거" (앞의 '라떼' 맥락 유지)

## 5. 설치 및 실행 가이드 (Installation & Usage)

### 5.1 환경 설정 (Environment Setup)

레포지토리 클론

git clone [https://github.com/your-org/ai-voice-kiosk.git](https://github.com/your-org/ai-voice-kiosk.git)
cd ai-voice-kiosk


가상 환경 생성 및 활성화

python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate  # Windows


의존성 패키지 설치

AI는 requirements.txt를 기반으로 필요한 패키지를 확인합니다.

pip install -r requirements.txt


환경 변수 설정 (.env)

.env.example 파일을 복사하여 .env를 생성하고 API 키를 입력하세요.

OPENAI_API_KEY=sk-proj-...
DB_PATH=./data/menu_db.sqlite


### 5.2 데이터베이스 초기화 (RAG 구축)

메뉴 데이터를 벡터 DB에 임베딩하는 과정입니다.

python src/data_ingestion.py


### 5.3 프로젝트 실행 (Run)

메인 애플리케이션(FastAPI 서버 또는 터미널 데모)을 실행합니다.

python src/main.py


### 6. 예시 시나리오 (Usage Scenario)

개발 및 테스트 시 아래 시나리오가 정상 작동하는지 확인합니다.

Scenario: 점심 메뉴 추천

사용자: "오늘 점심 메뉴 뭐야?"

System (STT): "오늘 점심 메뉴 뭐야?" 텍스트 변환

System (RAG): DB에서 '점심 특선', '추천 메뉴' 태그가 있는 데이터(카레라이스, 김치찌개) 검색

System (LLM): 검색 결과를 바탕으로 "오늘 점심 메뉴로는 카레라이스와 김치찌개가 준비되어 있습니다." 생성

사용자: "카레라이스랑 같이 먹을 음료 추천해줘."

System (LLM): '카레라이스' 컨텍스트 유지 + 음료 DB 검색 -> "카레의 맛을 깔끔하게 해줄 아이스 아메리카노나 탄산음료를 추천드려요."

## 7. 디렉토리 구조 (Directory Structure)

ai-voice-kiosk/
├── data/                  # 메뉴 데이터(JSON, SQLite) 및 벡터 DB 저장소
├── src/
│   ├── main.py            # 메인 실행 파일
│   ├── audio/             # STT/TTS 처리 모듈
│   ├── llm/               # LLM 인터페이스 및 프롬프트 템플릿
│   ├── rag/               # 벡터 DB 검색 및 임베딩 로직
│   └── utils/             # 공통 유틸리티
├── .env                   # API Key 등 환경 설정
├── requirements.txt       # 의존성 목록
└── README.md              # 프로젝트 문서

└── README.md              # 프로젝트 문서

