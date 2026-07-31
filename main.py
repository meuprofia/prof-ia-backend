from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

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
def gerar_quiz(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    
    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"Gere 10 questões de quiz sobre {topic} em formato JSON de lista com as chaves: pergunta, opcoes (lista de 4), resposta_correta, explicacao."
                    }]
                }]
            }
            res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
            if res.status_code == 200:
                texto = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                limpo = texto.replace("```json", "").replace("```", "").strip()
                inicio = limpo.find("[")
                fim = limpo.rfind("]")
                if inicio != -1 and fim != -1:
                    limpo = limpo[inicio:fim+1]
                return json.loads(limpo)
        except Exception:
            pass

    return [
        {
            "pergunta": f"Questão sobre {topic} #{i}",
            "opcoes": ["Alternativa A", "Alternativa B", "Alternativa C", "Alternativa D"],
            "resposta_correta": "Alternativa A",
            "explicacao": f"Explicação detalhada sobre {topic}."
        } for i in range(1, 11)
    ]

@app.post("/api/gemini/flashcards")
@app.post("/api/gemini/flashcards/")
def gerar_flashcards(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    
    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"Gere 10 flashcards sobre {topic} em formato JSON de lista contendo objetos com as chaves exatas: 'front' e 'back'."
                    }]
                }]
            }
            res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
            if res.status_code == 200:
                texto = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                limpo = texto.replace("```json", "").replace("```", "").strip()
                inicio = limpo.find("[")
                fim = limpo.rfind("]")
                if inicio != -1 and fim != -1:
                    limpo = limpo[inicio:fim+1]
                return json.loads(limpo)
        except Exception:
            pass

    return [
        {
            "front": f"Conceito {i} de {topic}",
            "back": f"Definição oficial gerada para o estudo de {topic}."
        } for i in range(1, 11)
    ]

@app.post("/api/gemini/chat")
@app.post("/api/gemini/chat/")
def chat(data: dict = None):
    data = data or {}
    message = data.get("message") or data.get("prompt") or "Olá"
    return {"result": f"Olá! Entendi sua mensagem sobre: {message}"}

@app.post("/api/gemini/redacao")
@app.post("/api/gemini/redacao/")
def redacao(data: dict = None):
    data = data or {}
    tema = data.get("tema") or data.get("topic") or "Geral"
    return {"result": f"Análise estruturada e dicas para a redação sobre o tema: {tema}."}

@app.post("/api/gemini/editor-refine")
@app.post("/api/gemini/editor-refine/")
def editor_refine(data: dict = None):
    data = data or {}
    return {"result": data.get("text") or "Texto revisado com sucesso."}

@app.post("/api/gemini/material")
@app.post("/api/gemini/material/")
def material(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    return {"result": f"Material de estudo completo sobre: {topic}."}
