from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import requests
from database import SessionLocal, ChatMessage

app = FastAPI()

REMOTE_SERVER_URL = "http://localhost:9000/"  # Change later on

# Get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get local chat history
@app.get("/chats/{chat_id}")
def get_chat(chat_id: str, db: Session = Depends(get_db)):
    return db.query(ChatMessage).filter(ChatMessage.chat_id == chat_id).order_by(ChatMessage.timestamp).all()

# Send message (Stores locally & forwards to Remote API)
@app.post("/chats/{chat_id}")
def send_message(chat_id: str, sender: str, message: str, db: Session = Depends(get_db)):
    new_message = ChatMessage(chat_id=chat_id, sender=sender, message=message)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    # Send message to remote RAG & LLM API
    response = requests.post(f"{REMOTE_SERVER_URL}/query", json={"chat_id": chat_id, "message": message})
    
    # Store response locally
    ai_response = ChatMessage(chat_id=chat_id, sender="AI", message=response.json()["response"])
    db.add(ai_response)
    db.commit()
    
    return ai_response