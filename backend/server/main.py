from fastapi import FastAPI
import chromadb  # Example vector database
import requests
import os
from fastapi.middleware.cors import CORSMiddleware
from retrievers import hybrid_similarity_search
from retrievers import semantic_search, refine_question_with_llm
from config import ServerConfig
from langdetect import detect


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
    question = data.get("message", "")
    conversation_history = data.get("content", "")

    use_hybrid = ServerConfig.use_hybrid
    llm_model = ServerConfig.llm_model
    embed_model = ServerConfig.embed_model
    vectorstore = ServerConfig.vectorstore
    bm25_retriever = ServerConfig.bm25_retriever

    # Retrieve relevant documents
    if use_hybrid:
        # Hybrid-Suche (falls aktiviert)
        # results = hybrid_similarity_search(
        #     question, conversation_history, embed_model, vectorstore, bm25_retriever
        # )
        pass
    else:
        # Refine the question using the LLM
        refined_question = refine_question_with_llm(question, conversation_history, llm_model)
        print("Refined question:", refined_question)

        # Perform semantic search using the refined question
        results = semantic_search(refined_question, vectorstore, embed_model)

    retrieved_sources = [result["source"] for result in results]
    retrieved_content = [result["content"] for result in results]
    content = " ".join(retrieved_content)  # Kontext für das LLM

    # Generate response with llm on question and additional content
    # Detect the language of the question
    question_language = detect(question)
    print("Question language:", question_language)

    # System prompt to instruct the LLM
    system_prompt = (
        f"You are an AI assistant that answers questions based on the provided context. "
        f"Respond in the same language as the user's question ({question_language}). "
        f"Your primary objective is to provide accurate answers using only the additional context. If the context does not fully address the question, politely inform the user and suggest rephrasing if necessary. Avoid using external knowledge or assumptions. "
        f"Here is the additional context, to help you answering the user question: {content} "
        f"Ensure that your response aligns with any previous messages in the conversation, if relevant. Chat history: {conversation_history} "
        f"If the context contains multiple sources, summarize key points concisely before answering. "
        f"Respond in well-structured Markdown. Format headings, lists, and code blocks appropriately. "
        f"Use bullet points for lists and bold or italics for emphasis."
    )
    # ---> Idea to use a parser or something like this to print llm response nicely

    # Conversation to send to the LLM
    conversation = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]

    chat_completion = llm_model.chat.completions.create(
        model="llama3-8b-8192",
        messages=conversation,
    )

    # ai_message = chat_completion.json()["choices"][0]["message"]["content"]
    ai_message = chat_completion.choices[0].message.content
    print("AI response:", ai_message)

    return {
        "response": ai_message,
        "sources": retrieved_sources,
        "content": retrieved_content
    }

@app.get("/config/models")
def get_model_config():
    """Retrieve the current model configuration."""
    return {
        "use_hybrid": ServerConfig.use_hybrid,
        "llm_model": str(ServerConfig.llm_model.__class__.__name__),
        "embed_model": str(ServerConfig.embed_model.__class__.__name__),
        "bm25_retriever": ServerConfig.bm25_retriever
    }

