from dotenv import load_dotenv
from service.parsing_service import JsonService
from utils.util import INTERVIEW_PROMPT_TYPE

load_dotenv()

if __name__ == "__main__":
    input_path = '../interview.json'
    output_path = '../file/interview.json'

    json_service = JsonService()
    json_service.process_json(input_path, output_path, INTERVIEW_PROMPT_TYPE)