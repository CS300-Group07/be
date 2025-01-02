import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    DB_PORT = os.environ.get('DB_PORT')
    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_DB = os.environ.get('POSTGRES_DB')
    DB_HOST = os.environ.get('DB_HOST')

    BACKEND_HOST = os.environ.get('BACKEND_HOST')
    BACKEND_PORT = os.environ.get('BACKEND_PORT')

    FRONTEND_HOST = os.environ.get('FRONTEND_HOST')
    FRONTEND_PORT = os.environ.get('FRONTEND_PORT')

    ### OpenAI settings
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    ASSISTANT_PROMPT = """
    You are a virtual assistant for the vbmatch app. Your primary role is to provide support to users by answering frequently asked questions (FAQs) and offering guidance on using vbmatch effectively. You help users understand features like product search, price comparison, and navigating the app. If a user has technical issues, provide troubleshooting steps or suggest contacting support.

    Always keep your responses concise, accurate, and focused on vbmatch-related topics.
    """
    ASSISTANT_MODEL = "gpt-4o-mini"