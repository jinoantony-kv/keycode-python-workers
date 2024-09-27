import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv(override=True)


GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY",None)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY",None)