import json
import os

class JsonV2Service:
    def __init__(self):
        pass

    def load_history(self, path: str):
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
            return data.get("conversation_history", [])
        return []

    def save_history(self, path: str, history_list) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({"conversation_history": history_list}, f, ensure_ascii=False, indent=4)


def get_json_v2_service() -> JsonV2Service:
    return JsonV2Service()
