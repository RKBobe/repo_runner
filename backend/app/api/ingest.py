from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
import shutil
import os
import subprocess
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone
from app.core.llm import configure_settings
from app.core.config import settings

router = APIRouter()

class IngestRequest(BaseModel):
    repo_url: str
    branch: str = "main"

def clone_and_process(repo_url: str, repo_id: str):
    local_path = f"./temp_repos/{repo_id}"
    
    # Clean up old runs
    if os.path.exists(local_path):
        shutil.rmtree(local_path)
    
    try:
        print(f"Cloning {repo_url}...")
        subprocess.check_call(["git", "clone", repo_url, local_path])
        print(f"Cloned to {local_path}")

        # 1. Configure Gemini (LLM & Embeddings)
        configure_settings()

        # 2. Read Files from the cloned repo
        # We filter for code files to avoid junk
        reader = SimpleDirectoryReader(
            input_dir=local_path,
            recursive=True,
            required_exts=[".py", ".js", ".ts", ".jsx", ".tsx", ".md", ".java", ".html", ".css"]
        )
        documents = reader.load_data()
        print(f"Loaded {len(documents)} documents.")

        # 3. Connect to Pinecone
        # Initialize the client using the key from settings
        pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        
        # Connect to your specific index
        # IMPORTANT: Make sure your index on Pinecone.io is named 'repo-runner'
        pinecone_index = pc.Index("repo-runner") 

        # 4. Create the Vector Store wrapper
        vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # 5. Index Data (This actually uploads the vectors to the cloud)
        print("Uploading vectors to Pinecone... this might take a minute.")
        index = VectorStoreIndex.from_documents(
            documents, 
            storage_context=storage_context
        )
        print("Successfully indexed to Pinecone!")
        
    except Exception as e:
        print(f"Error processing repo: {e}")

@router.post("/ingest")
async def ingest_repo(request: IngestRequest, background_tasks: BackgroundTasks):
    repo_name = request.repo_url.split("/")[-1].replace(".git", "")
    background_tasks.add_task(clone_and_process, request.repo_url, repo_name)
    return {"status": "processing", "message": f"Started ingestion for {repo_name}"}