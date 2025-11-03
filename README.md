# 🤖 AI Interview Bot

LangChain + Gradio 기반 AI 면접 시뮬레이터입니다.  
이력서 업로드 → 요약 → 질문 생성 → 답변 평가 → 피드백 보고서까지 자동화합니다.

## 🚀 실행 방법
```bash
pip install -r requirements.txt
def load_api_keys(filepath="api_key.txt"):
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()
load_api_keys(path + 'api_key.txt')
python app.py

## 환경 충돌시
pip install langchain_openai langchain_core langchain-community -q
pip install PyMuPDF
pip install python-docx
pip install -U langgraph
