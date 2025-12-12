# AI Voice Kiosk Project
## 실제 구현 화면
<img width="324" height="879" alt="스크린샷 2025-12-12 155917" src="https://github.com/user-attachments/assets/2a1ae24e-646f-4825-96e9-647be3607158" />

## 1. 개요 및 목적 (Overview & Purpose)
**AI Voice Kiosk**는 최신 생성형 AI 기술(LLM)과 음성 인식 기술(STT)을 결합하여, 사용자가 사람과 대화하듯이 자연스럽게 주문할 수 있는 차세대 키오스크 시스템입니다. 
기존의 터치 중심 키오스크가 가진 접근성 한계(복잡한 UI, 디지털 소외 계층의 어려움)를 해결하고, "불고기 버거 줘"와 같은 단순 명령부터 "느끼하지 않은 거 추천해줘" 같은 복잡한 요구사항까지 처리하는 것을 목표로 합니다.

---

## 2. 기술 스택 (Tech Stack)

### **Backend**
| Component | Tech | Description |
|-----------|------|-------------|
| Language | Python 3.10+ | 주 개발 언어 |
| Framework | FastAPI | 비동기 지원 고성능 웹 프레임워크 |
| Server | Uvicorn | ASGI 서버 |

### **AI Core**
| Component | Tech | Description |
|-----------|------|-------------|
| LLM | **Ollama** | 로컬 LLM 구동 (Gemma 3 12B 모델 사용) |
| RAG | **ChromaDB** | 벡터 검색을 통한 메뉴 추천 시스템 구축 |
| Embedding | Default | ChromaDB 내장 임베딩 모델 사용 |

### **Frontend**
| Component | Tech | Description |
|-----------|------|-------------|
| Core | HTML5, CSS3, JS | Vanilla JS를 이용한 SPA 형태의 동작 구현 |
| Voice | **Web Speech API** | 브라우저 내장 STT/TTS 엔진 (Chrome 권장) |

---

## 3. 설치 방법 (Installation)

1. **저장소 클론 (Clone Repository)**
   ```bash
   git clone [GitHub Repository Link Here]
   cd AI-Voice-Kiosk-Project
   ```

2. **Ollama 설치 및 모델 준비**
   - [Ollama 공식 홈페이지](https://ollama.com/)에서 다운로드 및 설치
   - 터미널에서 모델 다운로드:
     ```bash
     ollama pull gemma3:12b
     ```

3. **가상환경 설정 및 패키지 설치**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

---

## 4. 실행 방법 (Usage)

1. **Ollama 서버 실행** (별도 터미널)
   ```bash
   ollama serve
   ```

2. **키오스크 서버 실행**
   ```bash
   python -m src.main
   ```

3. **접속**
   - 브라우저를 열고 `http://localhost:8000` 접속
   - 마이크 권한 허용 필요

---

## 5. 제공 기능 (Features)

1.  **음성 주문 & 대화**: 사용자의 발화를 텍스트로 변환(STT)하여 AI가 이해하고 답변합니다.
2.  **스마트 장바구니 제어**: 대화만으로 메뉴 추가, 삭제, 초기화, 주문 완료가 가능합니다.
3.  **RAG 기반 메뉴 추천**: "상큼한 거 줘"라고 하면 벡터 DB에서 '레모네이드', '오렌지주스'를 찾아 추천합니다.
4.  **하이브리드 UI**: 터치 제어와 음성 제어가 완벽하게 동기화됩니다.
5.  **시각적 피드백**: 실시간 음성 인식 자막, 3단 레이아웃(메뉴-장바구니-채팅), 주문 내역 실시간 갱신.

---

## 6. GitHub 링크
- [https://github.com/kingy0ujin/AI-Voice-Kiosk-Project](https://github.com/kingy0ujin/AI-Voice-Kiosk-Project)
