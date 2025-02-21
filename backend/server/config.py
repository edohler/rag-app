import os
from dotenv import load_dotenv
from groq import Groq
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_chroma import Chroma
from rank_bm25 import BM25Okapi

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

class ServerConfig:
    """Stores and manages model configurations on the server."""

    LLM_API_KEY = os.environ.get("LLM_API_KEY")

    # Default models (can be changed via API)
    llm_model = Groq(api_key=LLM_API_KEY)
    embed_model = FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")
    vectorstore = Chroma(persist_directory=os.path.join('data/indexes', 'chroma'), embedding_function=embed_model)
    bm25_retriever = "BM250 retriever" # BM25Okapi(tokenized_corpus)
    use_hybrid = False

    @classmethod
    def update_config(cls, llm_model=None, embed_model=None, vectorstore=None, bm25_retriever=None, use_hybrid=None):
        """Allows dynamic updates to the model configuration."""
        if llm_model:
            cls.llm_model = llm_model
        if embed_model:
            cls.embed_model = embed_model
        if vectorstore:
            cls.vectorstore = vectorstore
        if bm25_retriever:
            cls.bm25_retriever = bm25_retriever
        if use_hybrid:
            cls.use_hybrid = use_hybrid