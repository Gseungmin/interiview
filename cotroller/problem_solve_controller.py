from dotenv import load_dotenv
from service.parsing_service import JsonService
from utils.util import PROBLEM_SOLVE_PROMPT_TYPE

load_dotenv()

if __name__ == "__main__":
    input_path = '../problem.json'
    output_path = '../file/problem.json'

    json_service = JsonService()
    json_service.process_json(input_path, output_path, PROBLEM_SOLVE_PROMPT_TYPE)