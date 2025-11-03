import random
from typing import Dict, List, Literal
from models.state_types import InterviewState

def decide_next_step(state: InterviewState) -> InterviewState:
    """규칙 기반 진행 제어: 영역 점수가 임계치 이상이면 다음 영역, 아니면 심화질문."""
    threshold = 0.75
    qs = state.get("question_strategy", {})
    seq = list(qs.keys())
    cur = state.get("current_strategy", (seq[0] if seq else ""))
    idx = (seq.index(cur) if cur in seq else 0)

    ev = state.get("evaluation", {})
    cur_field_scores = ev.get(cur, {})
    crits = ("구체성", "일관성", "적합성", "논리성")

    def _safe_int(x):
        try:
            return int(x)
        except Exception:
            return 0

    if isinstance(cur_field_scores, dict) and cur_field_scores.get("_n", 0) > 0:
        n = int(cur_field_scores["_n"])
        avg_specificity = cur_field_scores.get("_sum_구체성", 0) / n
        avg_consistency = cur_field_scores.get("_sum_일관성", 0) / n
        avg_fit        = cur_field_scores.get("_sum_적합성", 0) / n
        avg_logic      = cur_field_scores.get("_sum_논리성", 0) / n
        score = (avg_specificity + avg_consistency + avg_fit + avg_logic) / 4.0
    else:
        nums = [_safe_int(cur_field_scores.get(k, 0)) for k in crits] if isinstance(cur_field_scores, dict) else [0,0,0,0]
        score = sum(nums) / 4.0

    deep_counts = state.get("deep_counts", {})
    cur_deep = int(deep_counts.get(cur, 0))

    if (score >= threshold) or (cur_deep >= 2):
        if seq and idx >= len(seq) - 1:
            next_state = {**state, "next_step": "summarize", "deep_counts": deep_counts}
        else:
            next_strategy = seq[idx + 1]
            next_state = {
                **state,
                "next_step": "change_strategy",
                "current_strategy": next_strategy,
                "deep_counts": deep_counts
            }
    else:
        cur_deep += 1
        deep_counts[cur] = cur_deep
        next_state = {**state, "next_step": "generate", "deep_counts": deep_counts}

    return next_state


def change_strategy(state: InterviewState) -> InterviewState:
    """다음 분야로 전환하고 질문 하나를 선택."""
    qs = state.get("question_strategy", {})
    cur = state.get("current_strategy", "")
    block = qs.get(cur, {})
    questions = [v for v in block.values() if isinstance(v, str) and v.strip()]
    selected = random.choice(questions) if questions else "다음 분야 질문을 준비 중입니다."

    return {
        **state,
        "current_question": selected,
        "current_answer": "",
        "next_step": ""
    }


def route_next(state: InterviewState) -> Literal["generate", "change_strategy", "summarize"]:
    step = state.get("next_step", "additional_question")
    if step == "summarize" or step == "end":
        return "summarize"
    elif step == "change_strategy":
        return "change_strategy"
    else:
        return "generate"
