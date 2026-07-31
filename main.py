from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def chamar_gemini_direto(prompt: str):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY não configurada no Render.")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Erro na API do Gemini: {response.text}")
    
    data = response.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao parsear resposta do Gemini.")

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
    prompt = f"Gere exatamente 10 questões de quiz sobre {topic}. Retorne estritamente um JSON válido no formato de lista contendo objetos com as chaves exatas: 'pergunta', 'opcoes' (lista de 4 strings), 'resposta_correta' e 'explicacao'."
    
    texto_ia = chamar_gemini_direto(prompt)
    import json
    try:
        limpo = texto_ia.replace("```json", "").replace("```", "").strip()
        return json.loads(limpo)
    except:
        # Se a IA falhar em retornar JSON puro, criamos dinamicamente baseado no texto dela
        return [
            {
                "pergunta": f"Questão sobre {topic}",
                "opcoes": [texto_ia[:30], "Opção B", "Opção C", "Opção D"],
                "resposta_correta": texto_ia[:30],
                "explicacao": texto_ia
            }
        ]

@app.post("/api/gemini/flashcards")
@app.post("/api/gemini/flashcards/")
def gerar_flashcards(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    prompt = f"Gere exatamente 10 flashcards sobre {topic}. Retorne estritamente um JSON válido em formato de lista contendo objetos com as chaves exatas: 'front' e 'back'."
    
    texto_ia = chamar_gemini_direto(prompt)
    import json
    try:
        limpo = texto_ia.replace("```json", "").replace("```", "").strip()
        return json.loads(limpo)
    except:
        # Fallback dinâmico usando o texto real gerado pela IA
        return [
            {
                "front": f"Tópico: {topic}",
                "back": texto_ia
            }
        ]

@app.post("/api/gemini/chat")
@app.post("/api/gemini/chat/")
def chat(data: dict = None):
    data = data or {}
    message = data.get("message") or data.get("prompt") or "Olá"
    return {"result": chamar_gemini_direto(message)}

@app.post("/api/gemini/redacao")
@app.post("/api/gemini/redacao/")
def redacao(data: dict = None):
    data = data or {}
    tema = data.get("tema") or data.get("topic") or "Geral"
    return {"result": chamar_gemini_direto(f"Analise o tema de redação: {tema}")}

@app.post("/api/gemini/editor-refine")
@app.post("/api/gemini/editor-refine/")
def editor_refine(data: dict = None):
    data = data or {}
    texto_obj = data.get("text") or "Revisar"
    return {"result": chamar_gemini_direto(f"Melhore este texto: {texto_obj}")}

@app.post("/api/gemini/material")
@app.post("/api/gemini/material/")
def material(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    return {"result": chamar_gemini_direto(f"Crie um material de estudo completo sobre: {topic}")}
