# **RAG Application**

created by Erik Döhler, 28.01.2025 Bern

## **Description**

A modern **Retrieval-Augmented Generation (RAG)** system with a Quasar-based frontend and Python backend. It supports semantic search, metadata filtering, and document uploads for creating a custom knowledge base. The backend integrates with vector databases (e.g., ChromaDB) and LLMs for enhanced search and response generation.

---

## **Setup**

### **Frontend**

1. Navigate into the project folder:

   ```
   cd rag-project
   ```

2. Install dependencies:

   ```
   npm install
   ```

3. Configure Base URL of axios in .env.developement or .env.production if necessary

4. Run the development server:
   ```
   quasar dev
   ```

### **Backend**

1. Navigate to `backend/`:

   ```
   cd rag-project/backend
   ```

2. Set up a virtual environment:

   ```
   python -m venv venv
   venv/Scripts/activate
   ```

3. Install dependiencies:

   ```
   pip install -r requirements.txt
   ```

4. Create a .env file:

   ```
   LLM_API_KEY = your_LLM_api_key # for the LLM to generate the response
   SEM_CHUNK_API_KEY = your_second_LLM_api_key # for the semantic chunking
   ```

## **Future Enhancements**

Nearly everything, since this project is just at the beginning
