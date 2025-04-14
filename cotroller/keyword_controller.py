from dotenv import load_dotenv
from service.parsing_service import JsonService

load_dotenv()

if __name__ == "__main__":
    input_path = '../interview.json'
    output_path = '../file/keyword.json'

    json_service = JsonService()
    json_service.process_keywords(input_path, output_path)