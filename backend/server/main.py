from fastapi import FastAPI
import chromadb  # Example vector database
import requests
import os
from fastapi.middleware.cors import CORSMiddleware
from retrievers import hybrid_similarity_search
from retrievers import semantic_search, refine_question_with_llm
from config import ServerConfig


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this later in production to sepicifc domains)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize Vector Database (ChromaDB Example)
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="pdf_data")


@app.post("/query")
def query_llm(data: dict):
    # chat_id = data["chat_id"]
    # message = data["message"]
    # content = data["content"]
    
    # # Retrieve relevant context from the vector database
    # results = collection.query(query_texts=[message], n_results=3)
    # context = " ".join([doc["text"] for doc in results["documents"]])
    
    # # Send to OpenAI (or another LLM)
    # response = requests.post(
    #     "https://api.openai.com/v1/chat/completions",
    #     headers={"Authorization": f"Bearer {LLM_API_KEY}"},
    #     json={"model": "gpt-4", "messages": [{"role": "system", "content": context}, {"role": "user", "content": message}]}
    # )
    
    # return {"response": response.json()["choices"][0]["message"]["content"]}
    return {"response": ["Eine schöne Antwort"]}

@app.post("/retrieve")
def retrieve_rag(data: dict):
    question = data.get("message", "")
    conversation_history = data.get("content", "")
    use_hybrid = ServerConfig.use_hybrid
    llm_model = ServerConfig.llm_model
    embed_model = ServerConfig.embed_model
    vectorstore = ServerConfig.vectorstore
    bm25_retriever = ServerConfig.bm25_retriever

    if use_hybrid:
        # Retrieve relevant documents using hybrid search
        # results = hybrid_similarity_search(
        #     question, conversation_history, embed_model, vectorstore, bm25_retriever
        # )
        pass
    else:
        # Refine the question using the LLM
        # refined_question = refine_question_with_llm(question, conversation_history, llm_model)

        # Perform semantic search using the refined question
        # results = semantic_search(refined_question, vectorstore, embed_model)
        pass

    return {"sources": ["123", "456"], "content": ["es war ein mal", "vor langer langer zeit"]}


@app.get("/config/models")
def get_model_config():
    """Retrieve the current model configuration."""
    return {
        "use_hybrid": ServerConfig.use_hybrid,
        "llm_model": str(ServerConfig.llm_model.__class__.__name__),
        "embed_model": str(ServerConfig.embed_model.__class__.__name__),
        "bm25_retriever": ServerConfig.bm25_retriever
    }

