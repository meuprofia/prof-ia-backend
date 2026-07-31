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
    
    if not GEMINI_API_KEY:
        return [{"front": "Erro", "back": "GEMINI_API_KEY não configurada no Render."}]
    
    # ATUALIZADO PARA v1beta E gemini-1.5-flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
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
            return [{"front": f"Erro Google {res.status_code}", "back": res.text}]
        
        texto = res.json()["candidates"][0]["content"]["parts"][0]["text"]
        limpo = texto.replace("```json", "").replace("```", "").strip()
        inicio = limpo.find("[")
        fim = limpo.rfind("]")
        if inicio != -1 and fim != -1:
            limpo = limpo[inicio:fim+1]
        return json.loads(limpo)
    except Exception as e:
        return [{"front": "Erro interno", "back": str(e)}]
