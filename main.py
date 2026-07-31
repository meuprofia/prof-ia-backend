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

@app.post("/api/gemini/flashcards")
@app.post("/api/gemini/flashcards/")
def gerar_flashcards(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Gere exatamente 10 flashcards educacionais reais sobre o tema '{topic}'. Retorne APENAS um array JSON puro (começando com [ e terminando com ]), contendo exatamente as chaves 'front' e 'back' com conteúdo rico e detalhado sobre o assunto."
            }]
        }]
    }
    
    res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=20)
    
    if res.status_code != 200:
        return [{"front": f"Erro API Google ({res.status_code})", "back": res.text}]
    
    texto = res.json()["candidates"][0]["content"]["parts"][0]["text"]
    limpo = texto.replace("```json", "").replace("```", "").strip()
    inicio = limpo.find("[")
    fim = limpo.rfind("]")
    if inicio != -1 and fim != -1:
        limpo = limpo[inicio:fim+1]
    return json.loads(limpo)

@app.post("/api/gemini/quiz")
@app.post("/api/gemini/quiz/")
def gerar_quiz(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Gere 10 questões de quiz sobre {topic}. Retorne APENAS um array JSON puro com as chaves: 'pergunta', 'opcoes' (lista de 4), 'resposta_correta', 'explicacao'."
            }]
        }]
    }
    res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=20)
    texto = res.json()["candidates"][0]["content"]["parts"][0]["text"]
    limpo = texto.replace("```json", "").replace("```", "").strip()
    inicio = limpo.find("[")
    fim = limpo.rfind("]")
    if inicio != -1 and fim != -1:
        limpo = limpo[inicio:fim+1]
    return json.loads(limpo)

@app.post("/api/gemini/chat")
@app.post("/api/gemini/chat/")
def chat(data: dict = None):
    data = data or {}
    message = data.get("message") or data.get("prompt") or "Olá"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": message}]}]}
    res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=20)
    return {"result": res.json()["candidates"][0]["content"]["parts"][0]["text"]}

@app.post("/api/gemini/redacao")
@app.post("/api/gemini/redacao/")
def redacao(data: dict = None):
    data = data or {}
    tema = data.get("tema") or data.get("topic") or "Geral"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": f"Faça uma análise detalhada e dicas para redação sobre: {tema}"}]}]}
    res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=20)
    return {"result": res.json()["candidates"][0]["content"]["parts"][0]["text"]}

@app.post("/api/gemini/editor-refine")
@app.post("/api/gemini/editor-refine/")
def editor_refine(data: dict = None):
    data = data or {}
    texto_obj = data.get("text") or "Revisar"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": f"Melhore e corrija este texto: {texto_obj}"}]}]}
    res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=20)
    return {"result": res.json()["candidates"][0]["content"]["parts"][0]["text"]}

@app.post("/api/gemini/material")
@app.post("/api/gemini/material/")
def material(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": f"Crie um material de estudo completo sobre: {topic}"}]}]}
    res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=20)
    return {"result": res.json()["candidates"][0]["content"]["parts"][0]["text"]}
@app.post("/api/auth/login")
@app.post("/api/auth/login/")
def login(data: dict = None):
    data = data or {}
    email = data.get("email") or ""
    senha = data.get("senha") or ""
    
    # Validação básica temporária para liberar o seu acesso ao dashboard imediatamente
    if email:
        return {
            "success": True,
            "token": "fake-jwt-token-profia",
            "user": {
                "email": email,
                "name": "Gestor Prof IA",
                "plan": "free"
            }
        }
    return {"success": False, "message": "E-mail inválido"}
