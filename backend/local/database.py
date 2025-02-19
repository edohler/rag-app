from sqlalchemy import Column, String, Text, Integer, DateTime, JSON, create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
import os

# Ensure storage folder exists
if not os.path.exists("storage"):
    os.makedirs("storage")

# SQLite Database Connection
DATABASE_URL = "sqlite:///storage/chat_database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Chat Message Model
class ChatMessage(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, index=True)  # Unique chat session ID
    title = Column(String)  # Chat session title
    sender = Column(String)  # "User" or "AI"
    message = Column(Text)
    sources = Column(Text, nullable=True)  # Store multiple sources as a JSON string
    content = Column(Text, nullable=True)  # Store multiple retrieved paragraphs as JSON string
    timestamp = Column(DateTime, default=datetime.datetime.now())

# Create tables
Base.metadata.create_all(bind=engine)