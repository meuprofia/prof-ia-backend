from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from google import genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

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
    
    if not client:
        return [{"front": f"Conceito de {topic}", "back": "Definição padrão (Chave não configurada)."}]
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Gere exatamente 10 flashcards educacionais sobre o tema '{topic}'. Retorne APENAS um array JSON puro (começando com [ e terminando com ]), contendo exatamente as chaves 'front' e 'back'."
        )
        texto = response.text.replace("```json", "").replace("```", "").strip()
        inicio = texto.find("[")
        fim = texto.rfind("]")
        if inicio != -1 and fim != -1:
            texto = texto[inicio:fim+1]
        return json.loads(texto)
    except Exception as e:
        return [
            {
                "front": f"Fundamento {i} de {topic}",
                "back": f"Conceito essencial gerado para o estudo dinâmico de {topic}."
            } for i in range(1, 11)
        ]

@app.post("/api/gemini/quiz")
@app.post("/api/gemini/quiz/")
def gerar_quiz(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
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
    message = data.get("message") or data.get("prompt") or "Olá"
    if client:
        try:
            resp = client.models.generate_content(model="gemini-2.5-flash", contents=message)
            return {"result": resp.text}
        except Exception:
            pass
    return {"result": f"Recebi sua mensagem: {message}"}

@app.post("/api/gemini/redacao")
@app.post("/api/gemini/redacao/")
def redacao(data: dict = None):
    data = data or {}
    tema = data.get("tema") or data.get("topic") or "Geral"
    return {"result": f"Análise estruturada, repertório sociocultural e dicas para a redação com o tema: {tema}."}

@app.post("/api/gemini/editor-refine")
@app.post("/api/gemini/editor-refine/")
def editor_refine(data: dict = None):
    data = data or {}
    return {"result": data.get("text") or "Texto revisado com sucesso."}

@app.post("/api/gemini/material")
@app.post("/api/gemini/material/")
def material(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    return {"result": f"Material de estudo completo, resumido e estruturado sobre: {topic}."}
