from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    UPSTAGE_API_KEY: str = os.getenv("UPSTAGE_API_KEY")

settings = Settings()