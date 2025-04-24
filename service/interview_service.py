from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser

from few_shot.interview_dialog import interview_examples
from few_shot.problem_dialog import problem_examples
from utils.prompt_util import PROBLEM_INTERVIEW_SYSTEM_PROMPT, INTERVIEW_SYSTEM_PROMPT

class InterviewService:
    def __init__(self):
        pass

    def get_llm(self, model_name: str = 'o4-mini'):
        return ChatOpenAI(model_name=model_name)

    def create_few_shot_prompt(self, examples=interview_examples):
        example_prompt = ChatPromptTemplate.from_messages([
            ("human", "{input}"),
            ("ai", "{answer}"),
        ])
        return FewShotChatMessagePromptTemplate(
            example_prompt=example_prompt,
            examples=examples,
        )

    def create_qa_prompt(self, system_prompt: str, few_shot_prompt: FewShotChatMessagePromptTemplate):
        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            few_shot_prompt,
            ("human", "{input}"),
        ])

    def get_system_prompt(self, type):
        if type == 0:
            return INTERVIEW_SYSTEM_PROMPT

        if type == 1:
            return PROBLEM_INTERVIEW_SYSTEM_PROMPT

        return INTERVIEW_SYSTEM_PROMPT

    def get_few_shot_example(self, type):
        if type == 0:
            return interview_examples

        if type == 1:
            return problem_examples

        return interview_examples

    def get_llm_chain(self, llm, type):
        system_prompt = self.get_system_prompt(type)
        example = self.get_few_shot_example(type)
        few_shot_prompt = self.create_few_shot_prompt(examples=example)
        qa_prompt = self.create_qa_prompt(system_prompt=system_prompt, few_shot_prompt=few_shot_prompt)
        chain = qa_prompt | llm | StrOutputParser()
        return chain

    def get_ai_response(self, user_message: str, type: int):
        llm = self.get_llm()
        llm_chain = self.get_llm_chain(llm=llm, type=type)
        ai_response = llm_chain.invoke({"input": user_message})
        return ai_response

def get_interview_service() -> InterviewService:
    return InterviewService()