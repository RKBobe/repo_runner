from fastapi import APIRouter, HTTPException  # <--- THIS WAS MISSING
from pydantic import BaseModel
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone
from app.core.config import settings
from app.core.llm import configure_settings

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
async def chat_with_repo(request: ChatRequest):
    try:
        # 1. Configure Gemini
        configure_settings()

        # 2. Connect to Pinecone
        pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        pinecone_index = pc.Index("repo-runner")
        
        # 3. Load the Index
        vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

        # 4. Create the Query Engine
        query_engine = index.as_query_engine(similarity_top_k=5)

        # 5. Ask Gemini
        response = query_engine.query(request.query)
        
        return {"response": str(response)}

    except Exception as e:
        print(f"Error during chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))