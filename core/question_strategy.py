import random
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from models.state_types import InterviewState
from pydantic import BaseModel, Field
from typing import List

llm = ChatOpenAI(model="gpt-4.1-mini")

class QSItem(BaseModel):
    direction: str
    examples: List[str]

class QSOutput(BaseModel):
    experience: QSItem
    motivation: QSItem
    logic: QSItem

class QSMultiOutput(BaseModel):
    potential: QSOutput
    organization: QSOutput
    job: QSOutput

def generate_question_strategy(state: InterviewState) -> InterviewState:
    summary = state.get("resume_summary", "")
    keywords = state.get("resume_keywords", [])

    prompt = ChatPromptTemplate.from_messages([
        ("system", "3명의 면접관(A/B/C)에 대한 면접 질문 전략을 JSON으로 만드세요."),
        ("human", f"요약: {summary}\n키워드: {keywords}")
    ])

    chain = prompt | llm.with_structured_output(QSMultiOutput)
    result = chain.invoke({})
    strategy_dict = {
        "경험": {"A": result.potential.experience.examples[0]},
        "동기": {"A": result.potential.motivation.examples[0]},
        "논리": {"A": result.potential.logic.examples[0]},
    }
    state["question_strategy"] = strategy_dict
    return state

def preProcessing_Interview(file_path: str, extract_func, analyze_func) -> InterviewState:
    resume_text = extract_func(file_path)
    state: InterviewState = {
        "resume_text": resume_text,
        "resume_summary": "",
        "resume_keywords": [],
        "question_strategy": {},
        "current_question": "",
        "current_answer": "",
        "current_strategy": "",
        "conversation": [],
        "evaluation": [],
        "next_step": "",
        "deep_counts": {}
    }
    state = analyze_func(state)
    state = generate_question_strategy(state)
    categories = ["경험", "동기", "논리"]
    cat = categories[0]
    state["current_question"] = state["question_strategy"][cat]["A"]
    state["current_strategy"] = cat
    return state
