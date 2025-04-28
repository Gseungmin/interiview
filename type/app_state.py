from typing import TypedDict

class AgentState(TypedDict):
    query: str
    ai_question: str
    session_id: str
    prompt_type: int
    time: int
    history: list
    lastAiMessage: str
    answer: str