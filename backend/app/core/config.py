import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Repo Runner API"
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # AI / Vector DB
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY") # You'll likely need this for LlamaIndex

settings = Settings()