from fastapi import FastAPI
import chromadb  # Example vector database
import requests
import os

app = FastAPI()

# Initialize Vector Database (ChromaDB Example)
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="pdf_data")

LLM_API_KEY = os.getenv("LLM_API_KEY")

@app.post("/query")
def query_rag(data: dict):
    chat_id = data["chat_id"]
    message = data["message"]
    
    # Retrieve relevant context from the vector database
    results = collection.query(query_texts=[message], n_results=3)
    context = " ".join([doc["text"] for doc in results["documents"]])
    
    # Send to OpenAI (or another LLM)
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {LLM_API_KEY}"},
        json={"model": "gpt-4", "messages": [{"role": "system", "content": context}, {"role": "user", "content": message}]}
    )
    
    return {"response": response.json()["choices"][0]["message"]["content"]}