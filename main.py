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

def chamar_gemini(prompt: str):
    if not GEMINI_API_KEY:
        return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    try:
        res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=25)
        if res.status_code == 200:
            data = res.json()
            texto = data["candidates"][0]["content"]["parts"][0]["text"]
            limpo = texto.replace("```json", "").replace("```", "").strip()
            inicio = limpo.find("[")
            fim = limpo.rfind("]")
            if inicio != -1 and fim != -1:
                limpo = limpo[inicio:fim+1]
            return json.loads(limpo)
    except Exception:
        pass
    return None

@app.post("/api/gemini/flashcards")
@app.post("/api/gemini/flashcards/")
def gerar_flashcards(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    
    prompt = f"Gere exatamente 10 flashcards educacionais sobre '{topic}'. Retorne APENAS um array JSON puro (começando com [ e terminando com ]), onde cada objeto tem exatamente as chaves: 'front' e 'back'."
    
    resultado = chamar_gemini(prompt)
    if resultado:
        return resultado
        
    return [
        {
            "front": f"Conceito {i} de {topic}",
            "back": f"Definição detalhada e estudo focado sobre o tópico {topic}."
        } for i in range(1, 11)
    ]

@app.post("/api/gemini/quiz")
@app.post("/api/gemini/quiz/")
def gerar_quiz(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    
    prompt = f"Gere exatamente 10 questões de quiz sobre '{topic}'. Retorne APENAS um array JSON puro (começando com [ e terminando com ]), onde cada objeto tem as chaves: 'pergunta', 'opcoes' (uma lista com 4 strings), 'resposta_correta' (exatamente igual a uma das opcoes) e 'explicacao'."
    
    resultado = chamar_gemini(prompt)
    if resultado:
        return resultado
        
    return [
        {
            "pergunta": f"Questão prática sobre {topic} #{i}",
            "opcoes": ["Alternativa A", "Alternativa B", "Alternativa C", "Alternativa D"],
            "resposta_correta": "Alternativa A",
            "explicacao": f"Explicação detalhada sobre a matéria de {topic}."
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
