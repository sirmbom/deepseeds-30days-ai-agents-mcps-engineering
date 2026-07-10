import os
from  dotenv import load_dotenv

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")

if not gemini_key:
    raise ValueError("Error: Missing GEMINI_API_KEY in your .env file.")

openai_url = os.getenv("OPENAI_BASE_URL")

os.environ["OPENAI_BASE_URL"] = openai_url
openai_key = os.environ["OPENAI_API_KEY"] = gemini_key