from llama_index.llms.gemini import Gemini 
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import Settings

def get_llm(): 
    """
    Returns the Gemini Flash LLM
    """
    return Gemini(
        model = "gemini-flash-latest",
        temperature=0.1,
        max_tokens=2048
    )
    
def get_embedding_model():
    """
    Returns the Gemini Embedding Model
    """
    return GeminiEmbedding(
        model_name="models/text-embedding-004"
    )
    
def configure_settings():
    """
    Configures and returns LlamaIndex Settings with Gemini models
    """
    Settings.llm = get_llm()
    Settings.embed_model = get_embedding_model()
  
    