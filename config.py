import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', "")
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', "")