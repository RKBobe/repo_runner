import os
from dotenv import load_dotenv

#Load variables from .env file
load_dotenv()

# Get Key
api_key = os.getenv("PINECONE_API_KEY")

# Verify it loaded
if not api_key:
    raise ValueError("PINECONE_API_KEY not found in environment variables") 