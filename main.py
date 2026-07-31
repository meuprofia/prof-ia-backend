from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import google.generativeai as genai

app = FastAPI()

# Configuração do CORS para permitir requisições da Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar a IA do Gemini com a chave das variáveis de ambiente
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class PromptRequest(BaseModel):
    topic: str

@app.get("/")
def read_root():
    return {"status": "Backend do Prof IA rodando com sucesso!"}

@app.post("/api/gemini/quiz")
def gerar_quiz(data: PromptRequest):
    try:
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"Gere um quiz educacional sobre: {data.topic}"
        response = model.generate_content(prompt)
        return {"result": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/gemini/flashcards")
def gerar_flashcards(data: PromptRequest):
    try:
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"Gere flashcards de memorização sobre: {data.topic}"
        response = model.generate_content(prompt)
        return {"result": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
