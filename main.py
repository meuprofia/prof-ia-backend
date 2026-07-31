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

def chamar_gemini_real(prompt: str):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY não encontrada nas variáveis de ambiente do Render.")
    
    # Usando a versão v1 e o modelo padrão atualizado do Gemini
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        # Retorna o erro exato que o Google está enviando para sabermos se houve bloqueio/cota
        raise HTTPException(status_code=500, detail=f"Google API Error [{response.status_code}]: {response.text}")
    
    data = response.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao extrair resposta da IA: {str(e)} - Resposta: {data}")

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
    prompt = f"Gere exatamente 10 questões de quiz sobre {topic}. Retorne APENAS um array JSON puro (começando com [ e terminando com ]), onde cada objeto tem exatamente as chaves: 'pergunta', 'opcoes' (lista de 4 strings), 'resposta_correta' e 'explicacao'."
    
    texto = chamar_gemini_real(prompt)
    try:
        # Limpeza agressiva de marcações markdown
        limpo = texto.replace("```json", "").replace("```", "").strip()
        # Encontra o primeiro '[' e o último ']' para garantir que pega apenas o JSON
        inicio = limpo.find("[")
        fim = limpo.rfind("]")
        if inicio != -1 and fim != -1:
            limpo = limpo[inicio:fim+1]
        return json.loads(limpo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"O texto retornado pela IA não é um JSON válido: {texto}")

@app.post("/api/gemini/flashcards")
@app.post("/api/gemini/flashcards/")
def gerar_flashcards(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    prompt = f"Gere exatamente 10 flashcards sobre {topic}. Retorne APENAS um array JSON puro (começando com [ e terminando com ]), onde cada objeto tem exatamente as chaves: 'front' e 'back'."
    
    texto = chamar_gemini_real(prompt)
    try:
        limpo = texto.replace("```json", "").replace("```", "").strip()
        inicio = limpo.find("[")
        fim = limpo.rfind("]")
        if inicio != -1 and fim != -1:
            limpo = limpo[inicio:fim+1]
        return json.loads(limpo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"O texto retornado pela IA para flashcards não é um JSON válido: {texto}")

@app.post("/api/gemini/chat")
@app.post("/api/gemini/chat/")
def chat(data: dict = None):
    data = data or {}
    message = data.get("message") or data.get("prompt") or "Olá"
    return {"result": chamar_gemini_real(message)}

@app.post("/api/gemini/redacao")
@app.post("/api/gemini/redacao/")
def redacao(data: dict = None):
    data = data or {}
    tema = data.get("tema") or data.get("topic") or "Geral"
    return {"result": chamar_gemini_real(f"Faça uma análise detalhada, repertório sociocultural e dicas de redação para o tema: {tema}")}

@app.post("/api/gemini/editor-refine")
@app.post("/api/gemini/editor-refine/")
def editor_refine(data: dict = None):
    data = data or {}
    texto_obj = data.get("text") or "Revisar"
    return {"result": chamar_gemini_real(f"Melhore, corrija e aprimore este texto mantendo a coesão: {texto_obj}")}

@app.post("/api/gemini/material")
@app.post("/api/gemini/material/")
def material(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    return {"result": chamar_gemini_real(f"Crie um material de estudo completo, estruturado e didático em Markdown sobre: {topic}")}
