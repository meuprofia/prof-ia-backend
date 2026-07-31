from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import google.generativeai as genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

@app.get("/")
def read_root():
    return {"status": "OK"}

@app.post("/api/auth/login")
@app.post("/api/auth/login/")
def login(data: dict = None):
    return {
        "success": True,
        "token": "fake-token",
        "user": {"name": "Gestor", "email": "meuprofia@gmail.com"}
    }

@app.post("/api/gemini/quiz")
@app.post("/api/gemini/quiz/")
def gerar_quiz(data: dict):
    topic = data.get("topic") or data.get("assunto") or "Geral"
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Gere um quiz educacional sobre: {topic}")
        return {"result": response.text}
    except Exception as e:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(f"Gere um quiz educacional sobre: {topic}")
            return {"result": response.text}
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

@app.post("/api/gemini/flashcards")
@app.post("/api/gemini/flashcards/")
def gerar_flashcards(data: dict):
    topic = data.get("topic") or data.get("assunto") or "Geral"
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Gere flashcards sobre: {topic}")
        return {"result": response.text}
    except Exception as e:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(f"Gere flashcards sobre: {topic}")
            return {"result": response.text}
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))
