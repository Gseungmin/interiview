from typing import Literal

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from type.app_state import AgentState
from utils.user_response_prompt import user_response_check_prompt

class UserResponseService:
    def __init__(self):
        self.llm = ChatOpenAI(model_name='o4-mini')

    def check_user_response(self, state: AgentState) -> Literal['answer', 'more', 'none']:
        ai_question = state['ai_question']
        query = state['query']
        chain = user_response_check_prompt | self.llm | StrOutputParser()
        response = chain.invoke({'query': query, 'ai_question': ai_question})
        return response

def get_user_response_service(
) -> UserResponseService:
    return UserResponseService()