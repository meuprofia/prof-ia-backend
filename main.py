from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import google.generativeai as genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def chamar_gemini(prompt: str):
    if not GEMINI_API_KEY:
        return "Erro: GEMINI_API_KEY não configurada no Render."
    for nome_modelo in ["gemini-1.5-flash", "gemini-pro"]:
        try:
            model = genai.GenerativeModel(nome_modelo)
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text
        except Exception:
            continue
    return "Erro ao processar a requisição com a IA."

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
    texto = chamar_gemini(f"Gere um quiz educacional sobre: {topic}")
    return [{"pergunta": texto, "opcoes": ["A", "B", "C", "D"], "resposta_correta": "A", "explicacao": "Verifique o texto gerado."}]

@app.post("/api/gemini/flashcards")
@app.post("/api/gemini/flashcards/")
def gerar_flashcards(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    texto = chamar_gemini(f"Gere flashcards sobre: {topic}")
    return [{"front": f"Tópico: {topic}", "back": texto}]

@app.post("/api/gemini/chat")
@app.post("/api/gemini/chat/")
def chat(data: dict = None):
    data = data or {}
    message = data.get("message") or data.get("prompt") or "Olá"
    return {"result": chamar_gemini(message)}

@app.post("/api/gemini/redacao")
@app.post("/api/gemini/redacao/")
def redacao(data: dict = None):
    data = data or {}
    tema = data.get("tema") or data.get("topic") or "Geral"
    return {"result": chamar_gemini(f"Analise o tema de redação: {tema}")}

@app.post("/api/gemini/editor-refine")
@app.post("/api/gemini/editor-refine/")
def editor_refine(data: dict = None):
    data = data or {}
    texto_obj = data.get("text") or "Revisar"
    return {"result": chamar_gemini(f"Melhore este texto: {texto_obj}")}

@app.post("/api/gemini/material")
@app.post("/api/gemini/material/")
def material(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    return {"result": chamar_gemini(f"Crie um material de estudo completo sobre: {topic}")}
