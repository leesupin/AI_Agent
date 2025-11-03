from pydantic import BaseModel, Field
from typing import List, Literal

# 이력서 분석 결과
class ResumeAnalysis(BaseModel):
    summary: str = Field(..., description="이력서 주요 내용을 3~5문장으로 요약")
    keywords: List[str] = Field(..., description="핵심 역량 및 키워드 목록")

# 이진 채점 기준
Binary = Literal[0, 1]

class BinCriterion(BaseModel):
    score: Binary
    rationale: str

# 답변 평가
class FourCriteriaEval(BaseModel):
    specificity: BinCriterion
    consistency: BinCriterion
    fit: BinCriterion
    logic: BinCriterion

# 심화 질문
class DeepQuestion(BaseModel):
    question: str
