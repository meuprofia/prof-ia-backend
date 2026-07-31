from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
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

class PromptRequest(BaseModel):
    topic: str

class LoginRequest(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None

@app.get("/")
def read_root():
    return {"status": "Backend rodando perfeitamente!"}

def handle_login():
    return {
        "success": True,
        "token": "fake-jwt-token-12345",
        "access_token": "fake-jwt-token-12345",
        "token_type": "bearer",
        "user": {
            "email": "meuprofia@gmail.com",
            "name": "Gestor"
        }
    }

@app.post("/api/auth/login")
def login_route_1(data: LoginRequest = None):
    return handle_login()

@app.post("/login")
def login_route_2(data: LoginRequest = None):
    return handle_login()

@app.post("/auth/login")
def login_route_3(data: LoginRequest = None):
    return handle_login()

@app.post("/api/gemini/quiz")
def gerar_quiz(data: PromptRequest):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Gere um quiz educacional sobre: {data.topic}"
        response = model.generate_content(prompt)
        return {"result": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/gemini/flashcards")
def gerar_flashcards(data: PromptRequest):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Gere flashcards de memorização sobre: {data.topic}"
        response = model.generate_content(prompt)
        return {"result": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
