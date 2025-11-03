import gradio as gr
from core.resume_parser import extract_text_from_file, analyze_resume
from core.question_strategy import preProcessing_Interview
from models.state_types import InterviewState

def initialize_state():
    return {"state": None, "interview_started": False, "interview_ended": False, "chat_history": []}

def upload_and_initialize(file_obj, session_state):
    if file_obj is None:
        return session_state, "파일을 업로드해주세요."
    file_path = file_obj.name
    state = preProcessing_Interview(file_path, extract_text_from_file, analyze_resume)
    session_state["state"] = state
    session_state["interview_started"] = True
    first_q = state["current_question"]
    session_state["chat_history"].append(["🤖 AI 면접관", first_q])
    return session_state, session_state["chat_history"]

# 간단화된 예시 실행
with gr.Blocks() as demo:
    session_state = gr.State(value=initialize_state())
    gr.Markdown("# 🤖 AI 면접관\n이력서를 업로드하고 인터뷰를 시작하세요!")
    with gr.Row():
        file_input = gr.File(label="이력서 업로드")
        upload_btn = gr.Button("시작하기")
    chatbot = gr.Chatbot()
    upload_btn.click(upload_and_initialize, inputs=[file_input, session_state], outputs=[session_state, chatbot])
demo.launch(share=True)
