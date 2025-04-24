import json
import os
from service.interview_service import get_interview_service

class JsonService:
    def __init__(self):
        self.interview_service = get_interview_service()

    def load_keywords(self, input_path):
        try:
            with open(input_path, 'r', encoding='utf-8') as file:
                keywords = json.load(file)
                return keywords
        except FileNotFoundError:
            print(f"Input file not found: {input_path}")
            return None
        except json.JSONDecodeError:
            print(f"Invalid JSON in input file: {input_path}")
            return None

    def process_keyword(self, keyword, type):
        try:
            response = self.interview_service.get_ai_response(user_message=keyword, type=type)
            return {
                "keyword": keyword,
                "response": response
            }
        except Exception as e:
            print(f"키워드 응답 예외가 발생했습니다. '{keyword}': {str(e)}")
            return None

    def process_all_keywords(self, keywords, type):
        responses = []
        for i, keyword in enumerate(keywords):
            result = self.process_keyword(keyword=keyword, type=type)
            if result:
                responses.append(result)
        return responses

    def load_existing_responses(self, output_path):
        existing_responses = []
        if os.path.exists(output_path):
            try:
                with open(output_path, 'r', encoding='utf-8') as file:
                    existing_responses = json.load(file)
            except json.JSONDecodeError:
                print(output_path, " 경로의 JSON 파일이 잘못되었습니다")
        return existing_responses

    def save_responses(self, all_responses, output_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(all_responses, file, ensure_ascii=False, indent=2)

    def process_json(self, input_path, output_path, type):
        keywords = self.load_keywords(input_path)
        if not keywords:
            return

        new_responses = self.process_all_keywords(keywords=keywords, type=type)
        self.save_responses(new_responses, output_path)
        existing_responses = self.load_existing_responses(output_path)
        all_responses = existing_responses + new_responses
        self.save_responses(all_responses, output_path)

def get_json_service() -> JsonService:
    return JsonService()