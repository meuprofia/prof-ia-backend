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
                        "text": f"Gere exatamente 10 flashcards educacionais sobre o assunto: {topic}. Retorne APENAS um array JSON puro (começando com [ e terminando com ]), contendo objetos com as chaves exatas: 'front' (frente do card com o conceito) e 'back' (verso com a definição clara)."
                    }]
                }]
            }
            res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=15)
            if res.status_code == 200:
                candidatos = res.json().get("candidates", [])
                if candidatos:
                    texto = candidatos[0]["content"]["parts"][0]["text"]
                    limpo = texto.replace("```json", "").replace("```", "").strip()
                    inicio = limpo.find("[")
                    fim = limpo.rfind("]")
                    if inicio != -1 and fim != -1:
                        limpo = limpo[inicio:fim+1]
                    return json.loads(limpo)
        except Exception:
            pass

    # Fallback apenas se a API falhar totalmente
    return [
        {
            "front": f"Conceito de {topic}",
            "back": f"Definição padrão gerada pelo sistema."
        }
    ]

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
            res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=15)
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
            "pergunta": f"Questão sobre {topic}",
            "opcoes": ["Opção A", "Opção B", "Opção C", "Opção D"],
            "resposta_correta": "Opção A",
            "explicacao": "Explicação padrão."
        }
    ]

@app.post("/api/gemini/chat")
@app.post("/api/gemini/chat/")
def chat(data: dict = None):
    data = data or {}
    message = data.get("message") or data.get("prompt") or "Olá"
    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            payload = {"contents": [{"parts": [{"text": message}]}]}
            res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=15)
            if res.status_code == 200:
                return {"result": res.json()["candidates"][0]["content"]["parts"][0]["text"]}
        except Exception:
            pass
    return {"result": f"Olá! Recebi sua mensagem: {message}"}

@app.post("/api/gemini/redacao")
@app.post("/api/gemini/redacao/")
def redacao(data: dict = None):
    data = data or {}
    tema = data.get("tema") or data.get("topic") or "Geral"
    return {"result": f"Análise estruturada para o tema de redação: {tema}."}

@app.post("/api/gemini/editor-refine")
@app.post("/api/gemini/editor-refine/")
def editor_refine(data: dict = None):
    data = data or {}
    return {"result": data.get("text") or "Texto revisado."}

@app.post("/api/gemini/material")
@app.post("/api/gemini/material/")
def material(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    return {"result": f"Material de estudo sobre {topic}."}
