from fastapi import Depends
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from repository.session_repository import SessionRepository, get_session_repository
from utils.prompt_combine import get_system_prompt, get_few_shot_example

class InterviewV2Service:
    def __init__(
            self,
            session_repository: SessionRepository = Depends(get_session_repository)
    ):
        self.session_repository = session_repository
        self.llm = ChatOpenAI(model_name='o4-mini')

    def create_few_shot_prompt(
            self,
            examples
    ):
        example_prompt = ChatPromptTemplate.from_messages([
            ("human", "{input}"),
            ("ai", "{answer}"),
        ])
        return FewShotChatMessagePromptTemplate(
            example_prompt=example_prompt,
            examples=examples,
        )

    def create_qa_prompt(
            self,
            system_prompt: str,
            few_shot_prompt: FewShotChatMessagePromptTemplate
    ):
        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            few_shot_prompt,
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

    def create_conversation_chain(
            self,
            prompt_type: int,
            time: int
    ) -> RunnableWithMessageHistory:
        system_prompt = get_system_prompt(prompt_type, time)
        example = get_few_shot_example(prompt_type, time)

        few_shot_prompt = self.create_few_shot_prompt(examples=example)
        qa_prompt = self.create_qa_prompt(system_prompt=system_prompt, few_shot_prompt=few_shot_prompt)

        base_chain = qa_prompt | self.llm | StrOutputParser()

        conversational_rag_chain = RunnableWithMessageHistory(
            runnable=base_chain,
            get_session_history=lambda session_id: self.session_repository.get_session_history(session_id),
            input_messages_key="input",
            history_messages_key="chat_history",
        )

        return conversational_rag_chain

    def get_ai_response(
            self,
            session_id: str,
            user_message: str,
            prompt_type: int,
            time: int = 0,
    ) -> str:
        conversation_chain = self.create_conversation_chain(
            prompt_type=prompt_type,
            time=time
        )

        return conversation_chain.invoke(
            {"input": user_message},
            config={"configurable": {"session_id": session_id}},
        )

def get_interview_v2_service(
    session_repository: SessionRepository = Depends(get_session_repository)
) -> InterviewV2Service:
    return InterviewV2Service(session_repository)