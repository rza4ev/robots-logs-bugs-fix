import os

from dotenv import load_dotenv
from mistralai.client import Mistral


load_dotenv()

api_key = os.getenv("test")

print(api_key)