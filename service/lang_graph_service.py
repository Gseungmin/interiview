from typing import Literal

from fastapi import Depends
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from service.interview_v2_service import InterviewV2Service, get_interview_v2_service
from type.app_state import AgentState
from utils.user_response_prompt import user_response_check_prompt
from utils.util import MORE_PROMPT_TYPE, NONE_PROMPT_TYPE

class LangGraphService:
    def __init__(
        self,
        interview_service: InterviewV2Service = Depends(get_interview_v2_service),
    ):
        self.interview_service = interview_service
        self.llm = ChatOpenAI(model_name="o4-mini")
        self.graph = self.build_graph()

    def build_graph(self):
        builder = StateGraph(AgentState)

        builder.add_node("pre_process", self.pre_process)
        builder.add_node("generate", self.generate)
        builder.add_node("user_response_evaluation", self.user_response_evaluation)

        builder.add_edge(START, "pre_process")
        builder.add_conditional_edges("pre_process", self.progress_evaluation)
        builder.add_edge("user_response_evaluation", "generate")
        builder.add_edge("generate", END)

        graph = builder.compile()

        with open("../rag_graph.png", "wb") as f:
            f.write(graph.get_graph().draw_mermaid_png())

        return graph

    def pre_process(self, state: AgentState) -> AgentState:
        history = state.get("history", [])
        if history:
            last_entry = history[-1]
            ai_answer = last_entry.get("ai", "")
            state["ai_question"] = ai_answer
        return state

    def progress_evaluation(self, state: AgentState) -> Literal['generate', 'user_response_evaluation']:
        history = state['history']

        history_length = len(history)

        # 첫 대화인 경우
        if history_length == 0:
            return "generate"

        # 마지막 대화인 경우
        if history_length >= 6:
            return 'generate'

        return 'user_response_evaluation'

    def user_response_evaluation(self, state: AgentState) -> AgentState:
        query = state['query']
        ai_question = state['ai_question']

        chain = user_response_check_prompt | self.llm | StrOutputParser()
        response = chain.invoke({'query': query, 'ai_question': ai_question})

        if response == "more":
            state['prompt_type'] = MORE_PROMPT_TYPE
            return state

        if response == "none":
            state['prompt_type'] = NONE_PROMPT_TYPE
            return state

        return state

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
) -> LangGraphService:
    return LangGraphService(interview_service)