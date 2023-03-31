import openai
import os

def open_ai_init():
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    if not OPENAI_API_KEY:
        from dotenv import load_dotenv
        load_dotenv('./.env')
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    openai.api_key = OPENAI_API_KEY
