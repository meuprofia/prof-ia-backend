from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import json
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
    
    # Usando o endpoint OpenAI-compatível oficial do Google que aceita o modelo flash estável
    url = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gemini-1.5-flash",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=30)
        if res.status_code == 200:
            data = res.json()
            return data["choices"][0]["message"]["content"]
        else:
            print(f"Erro OpenAI-compatível: {res.text}")
    except Exception as e:
        print(f"Exceção: {e}")
        
    return None

@app.post("/api/gemini/flashcards")
@app.post("/api/gemini/flashcards/")
def gerar_flashcards(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    
    prompt = f"Gere exatamente 10 flashcards educacionais sobre '{topic}'. Retorne APENAS um array JSON puro (começando com [ e terminando com ]), onde cada objeto tem as chaves exatas 'front' e 'back'."
    
    resposta = chamar_gemini(prompt)
    if resposta:
        try:
            limpo = resposta.replace("```json", "").replace("```", "").strip()
            inicio = limpo.find("[")
            fim = limpo.rfind("]")
            if inicio != -1 and fim != -1:
                limpo = limpo[inicio:fim+1]
            return json.loads(limpo)
        except Exception as e:
            print(f"Erro no parse JSON: {e}")
            
    return [{"front": f"Erro de Conexão IA", "back": f"Não foi possível processar o tema {topic}."}]

@app.post("/api/gemini/quiz")
@app.post("/api/gemini/quiz/")
def gerar_quiz(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    
    prompt = f"Gere exatamente 10 questões de quiz sobre '{topic}'. Retorne APENAS um array JSON puro (começando com [ e terminando com ]), onde cada objeto tem as chaves: 'pergunta', 'opcoes' (lista com 4 strings), 'resposta_correta' e 'explicacao'."
    
    resposta = chamar_gemini(prompt)
    if resposta:
        try:
            limpo = resposta.replace("```json", "").replace("```", "").strip()
            inicio = limpo.find("[")
            fim = limpo.rfind("]")
            if inicio != -1 and fim != -1:
                limpo = limpo[inicio:fim+1]
            return json.loads(limpo)
        except Exception:
            pass
            
    return [
        {
            "pergunta": f"Questão sobre {topic} #1",
            "opcoes": ["Alternativa A", "Alternativa B", "Alternativa C", "Alternativa D"],
            "resposta_correta": "Alternativa A",
            "explicacao": "Explicação detalhada."
        }
    ]

@app.post("/api/gemini/chat")
@app.post("/api/gemini/chat/")
def chat(data: dict = None):
    data = data or {}
    msg = data.get("message") or "Olá"
    res = chamar_gemini(msg)
    return {"result": res or "Olá! Como posso ajudar?"}

@app.post("/api/gemini/redacao")
@app.post("/api/gemini/redacao/")
def redacao(data: dict = None):
    data = data or {}
    tema = data.get("tema") or "Geral"
    res = chamar_gemini(f"Faça uma análise de redação sobre: {tema}")
    return {"result": res or "Análise estruturada indisponível no momento."}

@app.post("/api/gemini/editor-refine")
@app.post("/api/gemini/editor-refine/")
def editor_refine(data: dict = None):
    data = data or {}
    texto = data.get("text") or ""
    res = chamar_gemini(f"Melhore este texto: {texto}")
    return {"result": res or texto}

@app.post("/api/gemini/material")
@app.post("/api/gemini/material/")
def material(data: dict = None):
    data = data or {}
    topic = data.get("topic") or "Geral"
    res = chamar_gemini(f"Crie material de estudo sobre: {topic}")
    return {"result": res or "Material gerado."}
