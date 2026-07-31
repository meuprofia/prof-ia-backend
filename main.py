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
    data = data or {}
    email = data.get("email") or ""
    if email:
        return {
            "success": True,
            "token": "fake-jwt-token-profia",
            "user": {"email": email, "name": "Gestor Prof IA", "plan": "free"}
        }
    return {"success": False, "message": "E-mail inválido"}

@app.post("/api/gemini/flashcards")
@app.post("/api/gemini/flashcards/")
def gerar_flashcards(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    
    if not GEMINI_API_KEY:
        return [{"front": "Erro", "back": "Chave GEMINI_API_KEY não configurada no Render."}]
    
    url = f"https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gemini-1.5-flash",
        "messages": [
            {
                "role": "user",
                "content": f"Gere exatamente 10 flashcards educacionais sobre '{topic}'. Retorne APENAS um array JSON puro (começando com [ e terminando com ]), onde cada item tem as chaves exatas 'front' e 'back'."
            }
        ]
    }
    
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=25)
        if res.status_code != 200:
            return [{"front": f"Erro HTTP {res.status_code}", "back": res.text}]
        
        resposta_json = res.json()
        texto = resposta_json["choices"][0]["message"]["content"]
        limpo = texto.replace("```json", "").replace("```", "").strip()
        inicio = limpo.find("[")
        fim = limpo.rfind("]")
        if inicio != -1 and fim != -1:
            limpo = limpo[inicio:fim+1]
        return json.loads(limpo)
    except Exception as e:
        return [{"front": "Erro interno no processamento", "back": str(e)}]

@app.post("/api/gemini/quiz")
@app.post("/api/gemini/quiz/")
def gerar_quiz(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    return [
        {
            "pergunta": f"Questão sobre {topic} #{i}",
            "opcoes": ["Alternativa A", "Alternativa B", "Alternativa C", "Alternativa D"],
            "resposta_correta": "Alternativa A",
            "explicacao": f"Explicação detalhada sobre {topic}."
        } for i in range(1, 11)
    ]

@app.post("/api/gemini/chat")
@app.post("/api/gemini/chat/")
def chat(data: dict = None):
    data = data or {}
    return {"result": "Olá! Como posso ajudar nos seus estudos hoje?"}

@app.post("/api/gemini/redacao")
@app.post("/api/gemini/redacao/")
def redacao(data: dict = None):
    data = data or {}
    return {"result": "Análise estruturada e dicas para o desenvolvimento da sua redação."}

@app.post("/api/gemini/editor-refine")
@app.post("/api/gemini/editor-refine/")
def editor_refine(data: dict = None):
    data = data or {}
    return {"result": data.get("text") or "Texto revisado."}

@app.post("/api/gemini/material")
@app.post("/api/gemini/material/")
def material(data: dict = None):
    data = data or {}
    return {"result": "Material de estudo gerado com sucesso."}
