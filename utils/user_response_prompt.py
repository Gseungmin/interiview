from langchain_core.prompts import PromptTemplate

user_response_check_prompt = PromptTemplate.from_template("""
    다음은 AI가 생성한 면접 질문에 대한 사용자의 응답을 분류하기 위한 프롬프트입니다.
    
    AI 면접 질문:
    {ai_question}
    
    사용자의 응답:
    {query}
    
    응답 유형:
    1. 질문에 대한 답변을 한 경우 정확히 'answer' 출력  
    2. 질문에 대한 이해를 위해 추가 정보를 요청한 경우 정확히 'more' 출력  
    3. 답변을 모르는 경우는 정확히 'none' 출력
    
    위 규칙에 따라 정확히 한 단어('answer', 'more', 'none')만 출력하세요.
""")
