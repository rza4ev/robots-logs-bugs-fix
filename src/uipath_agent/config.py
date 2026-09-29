import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(
    PROJECT_ROOT / ".env",
    override=True,
)

APP_NAME = os.getenv("APP_NAME")
ENVIRONMENT = os.getenv("ENVIRONMENT")
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")