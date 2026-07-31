from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import google.generativeai as genai
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
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

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
    
    prompt = f"Gere exatamente 10 questões de quiz sobre {topic}. Retorne estritamente um JSON válido no formato de lista, onde cada item tem as chaves: 'pergunta', 'opcoes' (lista de 4 strings), 'resposta_correta' e 'explicacao'."
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash", generation_config={"response_mime_type": "application/json"})
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception:
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            limpo = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(limpo)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

@app.post("/api/gemini/flashcards")
@app.post("/api/gemini/flashcards/")
def gerar_flashcards(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    
    prompt = f"Gere exatamente 10 flashcards sobre {topic}. Retorne estritamente um JSON válido no formato de lista, onde cada item tem exatamente as chaves: 'front' e 'back'."
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash", generation_config={"response_mime_type": "application/json"})
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception:
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            limpo = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(limpo)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

@app.post("/api/gemini/chat")
@app.post("/api/gemini/chat/")
def chat(data: dict = None):
    data = data or {}
    message = data.get("message") or data.get("prompt") or "Olá"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(message)
    return {"result": response.text}

@app.post("/api/gemini/redacao")
@app.post("/api/gemini/redacao/")
def redacao(data: dict = None):
    data = data or {}
    tema = data.get("tema") or data.get("topic") or "Geral"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Analise o tema de redação: {tema}")
    return {"result": response.text}

@app.post("/api/gemini/editor-refine")
@app.post("/api/gemini/editor-refine/")
def editor_refine(data: dict = None):
    data = data or {}
    texto_obj = data.get("text") or "Revisar"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Melhore este texto: {texto_obj}")
    return {"result": response.text}

@app.post("/api/gemini/material")
@app.post("/api/gemini/material/")
def material(data: dict = None):
    data = data or {}
    topic = data.get("topic") or data.get("assunto") or "Geral"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Crie um material de estudo estruturado sobre: {topic}")
    return {"result": response.text}
