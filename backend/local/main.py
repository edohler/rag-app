from fastapi import FastAPI, Depends
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
    allow_origins=["*"],  # Allow all origins (change this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

REMOTE_SERVER_URL = "http://localhost:9000/"  # Change later on

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
    rag_response = requests.post(f"{REMOTE_SERVER_URL}/retrieve", json={"message": message})
    retrieved_sources = ["123", "456"] # rag_response.get("sources", [])  # List of file paths
    retrieved_content = ["es war ein mal", "vor langer langer zeit"] # rag_response.get("content", [])  # List of retrieved paragraphs

    # Call LLM API (generates AI response)
    response = requests.post(f"{REMOTE_SERVER_URL}/query", json={"chat_id": chat_id, "message": message, "content": retrieved_content})
    ai_message = response.json()["response"]

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