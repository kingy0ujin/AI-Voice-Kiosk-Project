# AI Voice Kiosk Project Summary

## 1. 프로젝트 개요 (Overview)
이 프로젝트는 **로컬 LLM (Ollama)**과 **RAG (검색 증강 생성)** 기술을 활용한 **음성 인식 AI 키오스크**입니다.  
사용자는 화면 터치뿐만 아니라 자연스러운 대화(음성)로 메뉴를 추천받고, 주문을 추가하거나 취소할 수 있습니다.

---

## 2. 기술 스택 (Tech Stack)

### **Backend (서버)**
- **Language**: Python 3.10+
- **Framework**: FastAPI (비동기 웹 서버)
- **Server**: Uvicorn

### **AI & Data (인공지능 및 데이터)**
- **LLM (Large Language Model)**: [Ollama](https://ollama.com/) (로컬 구동)
  - **Model**: `gemma3:12b` (설정에서 변경 가능)
  - **Role**: 사용자 의도 파악, 메뉴 추천, 장바구니 제어 명령어 생성
- **RAG (Retrieval-Augmented Generation)**:
  - **Vector DB**: `ChromaDB` (메뉴 설명 및 특징 데이터 저장/검색)
  - **Process**: 질문 -> DB 검색 -> LLM 프롬프트 주입 -> 답변 생성

### **Frontend (클라이언트)**
- **Structure**: HTML5, CSS3
- **Logic**: Vanilla JavaScript (ES6+)
- **Communication**: Fetch API (JSON 통신)

### **Voice Interaction (음성 상호작용)**
- **STT (Speech-to-Text)**: **Web Speech API** (`webkitSpeechRecognition`)
  - 브라우저(Chrome) 내장 엔진 사용 (별도 서버 모델 X, 빠르고 정확함)
- **TTS (Text-to-Speech)**: **Web Speech API** (`speechSynthesis`)
  - 브라우저 내장 음성 합성 사용

---

## 3. 프로젝트 구조 (Project Structure)

```
AI-Voice-Kiosk-Project/
├── src/
│   ├── core/
│   │   └── config.py          # 환경변수 및 설정 관리 (Ollama URL, 모델명 등)
│   ├── llm/
│   │   └── client.py          # LLM API 연동 (OpenAI 호환 라이브러리 사용)
│   ├── rag/
│   │   └── vector_db.py       # ChromaDB 초기화 및 메뉴 검색 로직
│   ├── static/                # 프론트엔드 정적 파일
│   │   ├── index.html         # 메인 키오스크 화면 (3단 레이아웃)
│   │   ├── style.css          # UI 스타일링 (다크 모드, 반응형 채팅)
│   │   ├── script.js          # 프론트엔드 로직 (음성 인식, 장바구니 관리)
│   │   └── *.png              # 메뉴 이미지들 (버거, 음료 등)
│   └── main.py                # FastAPI 메인 엔트리포인트
├── data/                      # ChromaDB 데이터 저장소 (자동 생성)
├── test_llm.py                # LLM 연결 테스트 스크립트
├── requirements.txt           # Python 의존성 목록
├── SETUP_COMMANDS.md          # 설치 및 실행 가이드
└── .env                       # 환경변수 파일 (API Key 등)
```

---

## 4. 구현된 주요 기능 (Implemented Features)

### **1. AI 대화 및 주문 제어**
- **자연어 이해**: "배고픈데 뭐 먹지?", "느끼하지 않은 거 추천해줘" 같은 질문에 답변.
- **장바구니 제어 (Tool Use)**:
  - LLM이 대화 맥락을 이해하고 특수 태그를 출력하여 시스템을 제어합니다.
  - `[ADD: 메뉴명]`: 장바구니에 담기
  - `[REMOVE: 메뉴명]`: 장바구니에서 빼기
  - `[CLEAR]`: 초기화
  - `[ORDER_COMPLETE]`: 주문 완료

### **2. RAG 기반 메뉴 추천**
- 단순 메뉴명 매칭이 아니라, 메뉴의 **특징('달콤한', '매콤한', '시원한')**을 Vector DB에서 검색합니다.
- 예: "치즈 들어간 거 다 보여줘" -> DB에서 치즈 관련 메뉴들을 찾아 LLM에게 제공 -> 정확한 추천 가능.

### **3. 하이브리드 인터페이스 (Hybrid UI)**
- **Touch & Voice**: 화면의 탭/메뉴를 터치해서 주문할 수도 있고, 말로 주문할 수도 있습니다.
- 두 방식은 완벽하게 연동됩니다. (터치로 담고, 말로 취소 가능)

### **4. 고도화된 UI/UX**
- **3단 레이아웃**: [메뉴 탭] - [주문 내역] - [실시간 채팅]
- **실시간 피드백**: 음성 인식 중일 때 텍스트가 실시간으로 표시됨 (`interimResults`).
- **자동 스크롤**: 채팅이 길어지면 최신 메시지로 자동 포커스.

---

## 5. 실행 방법 (Quick Start)

1. **Ollama 실행 및 모델 다운로드**:
   ```bash
   ollama serve
   ollama pull gemma3:12b
   ```

2. **패키지 설치**:
   ```bash
   pip install -r requirements.txt
   ```

3. **서버 실행**:
   ```bash
   python -m src.main
   ```

4. **접속**:
   브라우저(Chrome 권장)에서 [http://localhost:8000](http://localhost:8000) 접속
