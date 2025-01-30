from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from the backend!"}

@app.post("/refine-question/")
def refine_question(question: str):
    # Beispiel-Endpunkt für Frageverarbeitung
    refined = f"Refined Question: {question}"
    return {"refined_question": refined}