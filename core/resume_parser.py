import fitz
import os
from docx import Document
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from models.schemas import ResumeAnalysis
from models.state_types import InterviewState

llm = ChatOpenAI(model="gpt-4.1-mini")

def extract_text_from_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        doc = fitz.open(file_path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text
    elif ext == ".docx":
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    else:
        raise ValueError("지원하지 않는 파일 형식입니다.")

def analyze_resume(state: InterviewState) -> InterviewState:
    resume_text = state["resume_text"]

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "당신은 인사 담당자입니다. 이력서 텍스트를 요약하고 주요 키워드를 추출하세요."),
        ("human", "{resume_text}")
    ])

    chain = prompt_template | llm.with_structured_output(ResumeAnalysis)
    result: ResumeAnalysis = chain.invoke({"resume_text": resume_text})

    state["resume_summary"] = result.summary
    state["resume_keywords"] = result.keywords
    return state
