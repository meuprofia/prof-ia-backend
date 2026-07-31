from fastapi import FastAPI, HTTPException
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
    
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY não configurada no Render.")
    
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Gere exatamente 10 questões de quiz sobre {topic}. Retorne APENAS um array JSON puro (começando com [ e terminando com ]), onde cada objeto tem exatamente as chaves: 'pergunta', 'opcoes' (lista de 4 strings), 'resposta_correta' e 'explicacao'."
            }]
        }]
    }
    
    try:
        res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=15)
        if res.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Erro do Google: {res.text}")
        
        texto = res.json()["candidates"][0]["content"]["parts"][0]["text"]
        limpo = texto.replace("```json", "").replace("```", "").strip()
        inicio = limpo.find("[")
        fim = limpo.rfind("]")
        if inicio != -1 and fim != -1:
            limpo = limpo[inicio:fim+1]
        return json.loads(limpo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar quiz: {str(e)}")

@app.post("/api/gemini/flashcards")
@app.post("/api/gemini/flashcards/")
def gerar_flashcards(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY não configurada no Render.")
    
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Gere exatamente 10 flashcards sobre {topic}. Retorne APENAS um array JSON puro (começando com [ e terminando com ]), onde cada objeto tem exatamente as chaves: 'front' e 'back'."
            }]
        }]
    }
    
    try:
        res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=15)
        if res.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Erro do Google: {res.text}")
        
        texto = res.json()["candidates"][0]["content"]["parts"][0]["text"]
        limpo = texto.replace("```json", "").replace("```", "").strip()
        inicio = limpo.find("[")
        fim = limpo.rfind("]")
        if inicio != -1 and fim != -1:
            limpo = limpo[inicio:fim+1]
        return json.loads(limpo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar flashcards: {str(e)}")

@app.post("/api/gemini/chat")
@app.post("/api/gemini/chat/")
def chat(data: dict = None):
    data = data or {}
    message = data.get("message") or data.get("prompt") or "Olá"
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": message}]}]}
    res = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    return {"result": res.json()["candidates"][0]["content"]["parts"][0]["text"]}

@app.post("/api/gemini/redacao")
@app.post("/api/gemini/redacao/")
def redacao(data: dict = None):
    data = data or {}
    tema = data.get("tema") or data.get("topic") or "Geral"
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": f"Faça uma análise detalhada e dicas de redação para: {tema}"}]}]}
    res = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    return {"result": res.json()["candidates"][0]["content"]["parts"][0]["text"]}

@app.post("/api/gemini/editor-refine")
@app.post("/api/gemini/editor-refine/")
def editor_refine(data: dict = None):
    data = data or {}
    texto_obj = data.get("text") or "Revisar"
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": f"Melhore e corrija este texto: {texto_obj}"}]}]}
    res = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    return {"result": res.json()["candidates"][0]["content"]["parts"][0]["text"]}

@app.post("/api/gemini/material")
@app.post("/api/gemini/material/")
def material(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": f"Crie um material de estudo completo sobre: {topic}"}]}]}
    res = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    return {"result": res.json()["candidates"][0]["content"]["parts"][0]["text"]}
