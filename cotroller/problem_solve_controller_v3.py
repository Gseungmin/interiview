import uuid

from dotenv import load_dotenv

from repository.session_repository import get_session_repository
from service.interview_v2_service import get_interview_v2_service
from service.json_v2_service import get_json_v2_service
from service.lang_graph_service import get_lang_graph_service
from utils.util import MAX_INTERVIEW, PROBLEM_SOLVE_PROMPT_TYPE

load_dotenv()

if __name__ == "__main__":
    session_repository= get_session_repository()
    interview_service = get_interview_v2_service(session_repository)
    json_service = get_json_v2_service()

    lang_graph_service = get_lang_graph_service(
        interview_service=interview_service
    )

    history_file = "../file/chat_concept.json"
    session_id = str(uuid.uuid4())
    prompt_type = PROBLEM_SOLVE_PROMPT_TYPE

    is_first = True
    time = 0
    conversation_history = []
    all_sessions = json_service.load_history(history_file)

    while time < MAX_INTERVIEW:
        if is_first:
            user_input = input("키워드를 입력해주세요 : ").strip()
        else:
            user_input = input("답변을 입력해주세요 : ").strip()

        if user_input.lower() in ("exit", "quit"):
            break

        ai_answer = lang_graph_service.answer(
            query=user_input,
            session_id=session_id,
            prompt_type=prompt_type,
            time=time,
            history=conversation_history,
        )

        print("AI 응답 : ", ai_answer)

        conversation_history.append({
            "user": user_input,
            "ai": ai_answer
        })

        is_first = False
        time += 1

    all_sessions.append(conversation_history)
    json_service.save_history(history_file, all_sessions)