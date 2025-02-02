from fastapi import FastAPI
import chromadb  # Example vector database
import requests
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize Vector Database (ChromaDB Example)
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="pdf_data")

LLM_API_KEY = os.getenv("LLM_API_KEY")

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
    message = data["message"]

    return {"sources": ["123", "456"], "content": ["es war ein mal", "vor langer langer zeit"]}

