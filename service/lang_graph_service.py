from typing import Literal

from fastapi import Depends
from langchain_openai import ChatOpenAI
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from service.interview_v2_service import InterviewV2Service, get_interview_v2_service
from service.user_response_service import get_user_response_service, UserResponseService
from type.app_state import AgentState


class LangGraphService:
    def __init__(
        self,
        interview_service: InterviewV2Service = Depends(get_interview_v2_service),
        user_response_service: UserResponseService = Depends(get_user_response_service),
    ):
        self.interview_service = interview_service
        self.user_response_service = user_response_service
        self.llm = ChatOpenAI(model_name="o4-mini")
        self.graph = self.build_graph()

    def build_graph(self):
        builder = StateGraph(AgentState)

        builder.add_node("pre_process", self.pre_process)
        builder.add_node("generate", self.generate)
        builder.add_node("tail", self.generate)

        builder.add_edge(START, "pre_process")
        builder.add_conditional_edges("pre_process", self.progress)
        builder.add_edge("tail", END)
        builder.add_edge("generate", END)

        graph = builder.compile()
        with open("rag_graph.png", "wb") as f:
            f.write(graph.get_graph().draw_mermaid_png())

        return graph

    def pre_process(self, state: AgentState) -> AgentState:
        history = state.get("history", [])
        if history:
            last_entry = history[-1]
            ai_answer = last_entry.get("ai", "")
            state["ai_question"] = ai_answer
        return state

    def progress(self, state: AgentState) -> Literal['generate', 'tail']:
        history = state['history']

        history_length = len(history)

        # 첫 대화인 경우
        if history_length == 0:
            return "generate"

        # 마지막 대화인 경우
        if history_length >= 6:
            return 'generate'

        return 'tail'

    def generate(self, state: AgentState) -> AgentState:
        session_id = state['session_id']
        query = state['query']
        prompt_type = state['prompt_type']
        time = state['time']

        conversation_chain = self.interview_service.create_conversation_chain(
            prompt_type=prompt_type,
            time=time
        )

        answer = conversation_chain.invoke(
            {"input": query},
            config={"configurable": {"session_id": session_id}},
        )
        state["answer"] = answer
        return state

    def answer(
        self,
        query: str,
        session_id: str,
        prompt_type: int,
        time: int,
        history: list,
    ) -> str:
        result = self.graph.invoke(
            {
                "query": query,
                "session_id": session_id,
                "prompt_type": prompt_type,
                "time": time,
                "history": history,
            }
        )
        return result["answer"]

def get_lang_graph_service(
    interview_service: InterviewV2Service = Depends(get_interview_v2_service),
    user_response_service: UserResponseService = Depends(get_user_response_service)
) -> LangGraphService:
    return LangGraphService(interview_service, user_response_service)