import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenRouter API Key securely
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Ensure API key is set
if not OPENROUTER_API_KEY:
    raise ValueError("⚠️ OpenRouter API Key is missing! Please set OPENROUTER_API_KEY in your .env file.")

# Define ChromaDB storage path
CHROMA_DB_PATH = "./chroma_db"

#print(OPENAI_API_KEY)