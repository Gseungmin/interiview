# 키워드 기반 AI 면접 질문 생성

## 서비스 개요
1. 핵심 키워드를 기반으로 면접 질문을 생성
2. 단순히 개념이 넘어서 문제상황에 맞춘 추론 능력을 테스트

## 프로세스
1. .env 파일에 GPT API 삽입, 이때 env_config.py 파일 참고
2. 원하는 키워드에 대해 interview.json 파일에 삽입
3. interview.json 파일 실행
4. 시간이 지나면 file 경로에 keyword.json 파일 생성
