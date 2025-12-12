# 프로젝트 설정 및 실행 가이드

이 프로젝트는 Python 기반의 AI 음성 키오스크 시스템입니다. 
로컬 LLM (Ollama)을 사용하여 사용자의 응답을 처리합니다.

## 필수 요구 사항

- Python 3.9 이상
- [Ollama](https://ollama.com/) 설치 및 실행 중일 것

## 1. 가상환경 생성 및 활성화

프로젝트 루트 디렉토리(`C:\Users\211\Desktop\kiosk\AI-Voice-Kiosk-Project`)에서 터미널(PowerShell 또는 CMD)을 열고 다음 명령어를 실행하세요.

```powershell
# 가상환경 생성 (.venv 폴더가 생성됩니다)
python -m venv .venv

# 가상환경 활성화 (PowerShell)
.\.venv\Scripts\Activate.ps1

# (참고) 만약 실행 정책 오류가 발생하면 아래 명령어를 먼저 실행하세요
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

## 2. 패키지 설치

가상환경이 활성화된 상태(프롬프트 앞에 `(.venv)`가 표시됨)에서 필요한 라이브러리를 설치합니다.

```powershell
pip install -r requirements.txt
```

## 3. Ollama 설정 및 실행

이 프로젝트는 기본적으로 `llama3` 모델을 사용하도록 설정되어 있습니다. 
새 터미널을 열어 Ollama가 실행 중인지 확인하고 모델을 다운로드하세요.

```powershell
# Ollama 서버 실행 (백그라운드에서 실행 중이면 생략 가능)
ollama serve

# 모델 다운로드 (이미 다운로드 받았다면 생략 가능)
ollama pull llama3
```

> **참고**: 다른 모델을 사용하려면 `src/core/config.py`의 `LLM_MODEL` 값을 변경하거나 환경 변수를 설정하세요.

## 4. 메인 애플리케이션 실행

모든 설정이 완료되면 API 서버를 실행합니다.

```powershell
python -m src.main
```

실행 후 브라우저에서 `http://localhost:8000/health` 에 접속하여 서버 상태를 확인할 수 있습니다.
