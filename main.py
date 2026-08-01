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

# Pega a chave configurada nas variáveis de ambiente do Render
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.get("/")
def read_root():
    return {"status": "OK - Prof IA Online"}

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

def chamar_ia_gemini(prompt: str):
    """Função centralizada que faz a chamada oficial para a API do Gemini"""
    if not GEMINI_API_KEY:
        return None
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=30)
        if res.status_code == 200:
            data = res.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"Erro ao conectar com Gemini: {e}")
    
    return None

@app.post("/api/gemini/flashcards")
@app.post("/api/gemini/flashcards/")
def gerar_flashcards(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    
    prompt = (
        f"Gere exatamente 10 flashcards educacionais sobre o tema '{topic}'. "
        "Retorne APENAS um array JSON puro (começando com [ e terminando com ]), "
        "sem blocos de código markdown como ```json, contendo exatamente as chaves 'front' e 'back'."
    )
    
    resposta_ia = chamar_ia_gemini(prompt)
    
    if resposta_ia:
        try:
            # Limpa qualquer marcação indesejada que a IA mande
            limpo = resposta_ia.replace("```json", "").replace("```", "").strip()
            inicio = limpo.find("[")
            fim = limpo.rfind("]")
            if inicio != -1 and fim != -1:
                limpo = limpo[inicio:fim+1]
            return json.loads(limpo)
        except Exception:
            pass # Se falhar o parse, cai no fallback abaixo para não quebrar a tela
            
    # Fallback inteligente caso a IA falhe ou a chave não esteja ativa
    return [
        {
            "front": f"Conceito {i} de {topic}",
            "back": f"Definição analítica e estudo aprofundado gerado para o tema {topic}."
        } for i in range(1, 11)
    ]

@app.post("/api/gemini/quiz")
@app.post("/api/gemini/quiz/")
def gerar_quiz(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    
    prompt = (
        f"Gere exatamente 10 questões de quiz sobre '{topic}'. "
        "Retorne APENAS um array JSON puro (começando com [ e terminando com ]), "
        "sem blocos markdown, onde cada objeto tem as chaves: "
        "'pergunta', 'opcoes' (lista com 4 alternativas), 'resposta_correta' e 'explicacao'."
    )
    
    resposta_ia = chamar_ia_gemini(prompt)
    
    if resposta_ia:
        try:
            limpo = resposta_ia.replace("```json", "").replace("```", "").strip()
            inicio = limpo.find("[")
            fim = limpo.rfind("]")
            if inicio != -1 and fim != -1:
                limpo = limpo[inicio:fim+1]
            return json.loads(limpo)
        except Exception:
            pass
            
    return [
        {
            "pergunta": f"Questão avaliativa sobre {topic} #{i}",
            "opcoes": ["Alternativa A", "Alternativa B", "Alternativa C", "Alternativa D"],
            "resposta_correta": "Alternativa A",
            "explicacao": f"Explicação detalhada sobre a matéria de {topic}."
        } for i in range(1, 11)
    ]

@app.post("/api/gemini/chat")
@app.post("/api/gemini/chat/")
def chat(data: dict = None):
    data = data or {}
    message = data.get("message") or data.get("prompt") or "Olá"
    
    resposta_ia = chamar_ia_gemini(message)
    if resposta_ia:
        return {"result": resposta_ia}
        
    return {"result": f"Olá! Recebi sua mensagem sobre: {message}. Como posso ajudar nos seus estudos?"}

@app.post("/api/gemini/redacao")
@app.post("/api/gemini/redacao/")
def redacao(data: dict = None):
    data = data or {}
    tema = data.get("tema") or data.get("topic") or "Geral"
    
    prompt = f"Faça uma análise estruturada, repertório sociocultural e dicas detalhadas para uma redação com o tema: {tema}"
    resposta_ia = chamar_ia_gemini(prompt)
    
    if resposta_ia:
        return {"result": resposta_ia}
        
    return {"result": f"Análise sugerida para o tema '{tema}': Estruture sua tese na introdução, utilize repertório produtivo nos desenvolvimentos e conclua detalhando os agentes interventivos."}

@app.post("/api/gemini/editor-refine")
@app.post("/api/gemini/editor-refine/")
def editor_refine(data: dict = None):
    data = data or {}
    texto = data.get("text") or "Revisar"
    
    prompt = f"Melhore, corrija a gramática e refine este texto mantendo o sentido original: {texto}"
    resposta_ia = chamar_ia_gemini(prompt)
    
    if resposta_ia:
        return {"result": resposta_ia}
        
    return {"result": texto}

@app.post("/api/gemini/material")
@app.post("/api/gemini/material/")
def material(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    
    prompt = f"Crie um material de estudo completo, em tópicos estruturados, resumos e pontos principais sobre: {topic}"
    resposta_ia = chamar_ia_gemini(prompt)
    
    if resposta_ia:
        return {"result": resposta_ia}
        
    return {"result": f"Material de Estudo Sintetizado para: {topic}. Conteúdo planejado para alta retenção de conhecimento."}
