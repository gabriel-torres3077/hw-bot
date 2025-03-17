import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()

TELEGRAM_TOKEN_KEY=os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID=os.getenv("TELEGRAM_CHAT_ID")
FETCH_TIME=os.getenv("FETCH_TIME")