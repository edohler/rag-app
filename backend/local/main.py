from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import requests
from database import SessionLocal, ChatMessage
import json
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class MessageRequest(BaseModel):
    sender: str
    message: str
    
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this later in production to sepicifc domains)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

REMOTE_SERVER_URL = "http://localhost:8080"  # Change later on

# Get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all chat sessions
@app.get("/chats")
def get_chats(db: Session = Depends(get_db)):
    chats = db.query(ChatMessage.chat_id).distinct().all()
    
    # Convert list of tuples to structured JSON
    chat_list = [{"id": chat.chat_id, "title": f"Chat {idx+1}"} for idx, chat in enumerate(chats)]
    
    return chat_list if chat_list else []

# Get messages from a chat
@app.get("/chats/{chat_id}")
def get_chat(chat_id: str, db: Session = Depends(get_db)):
    messages = db.query(ChatMessage).filter(ChatMessage.chat_id == chat_id).order_by(ChatMessage.timestamp).all()

    return [
        {
            "sender": msg.sender,
            "message": msg.message,
            "sources": json.loads(msg.sources) if msg.sources else [],
            "content": json.loads(msg.content) if msg.content else []
        }
        for msg in messages
    ]

# Send message & forward to remote API
@app.post("/chats/{chat_id}")
def send_message(chat_id: str, request: MessageRequest, db: Session = Depends(get_db)):
    sender = request.sender
    message = request.message
    # Save user message
    new_message = ChatMessage(chat_id=chat_id, sender=sender, message=message)
    db.add(new_message)
    print("ID: " + chat_id)
    print("sender: " + sender)
    print("message: " + message)

    # Call RAG API (retrieves relevant files)
    try:
        rag_response = requests.post(f"{REMOTE_SERVER_URL}/retrieve", json={"message": message})
        rag_response.raise_for_status() 
        rag_data = rag_response.json()  # Ensure response is valid JSON
        retrieved_sources = rag_data.get("sources", [])
        retrieved_content = rag_data.get("content", [])
    except requests.exceptions.RequestException as e:
        print(f"Error calling RAG API: {e}")
        retrieved_sources = []
        retrieved_content = []

    # Call LLM API (generates AI response)
    try:
        response = requests.post(f"{REMOTE_SERVER_URL}/query", json={"chat_id": chat_id, "message": message, "content": retrieved_content})
        response.raise_for_status()
        llm_data = response.json()  # Ensure response is valid JSON
        ai_message = llm_data.get("response", "Error: No response from AI.")

        if isinstance(ai_message, list):
            ai_message = " ".join(ai_message)
    except requests.exceptions.RequestException as e:
        print(f"Error calling LLM API: {e}")
        ai_message = "Error: LLM service unavailable."

    # Store AI response with sources
    ai_response = ChatMessage(
        chat_id=chat_id,
        sender="AI",
        message=ai_message,
        sources=json.dumps(retrieved_sources),  # Store as JSON string
        content=json.dumps(retrieved_content)   # Store as JSON string
    )
    db.add(ai_response)
    db.commit()

    return {"sender": "AI", "message": ai_message, "sources": retrieved_sources, "content": retrieved_content}

@app.delete("/chats/{chat_id}")
async def delete_chat(chat_id: str, db: Session = Depends(get_db)):
    # print({chat_id})
    deleted_rows = db.query(ChatMessage).filter(ChatMessage.chat_id == chat_id).delete(synchronize_session=False)
    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    db.commit()
    return {"message": "Chat deleted successfully"}