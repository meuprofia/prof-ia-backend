from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    client = genai.Client(api_key=API_KEY)
else:
    client = None


class FlashcardRequest(BaseModel):
    topic: str


@app.get("/")
def home():
    return {"status": "online"}


@app.post("/api/gemini/flashcards")
def gerar_flashcards(req: FlashcardRequest):

    if client is None:
        return {
            "error": "A variável GEMINI_API_KEY não foi configurada."
        }

    prompt = f"""
Crie exatamente 10 flashcards sobre "{req.topic}".

Retorne SOMENTE um JSON válido.

Formato:

[
  {{
    "front":"Pergunta",
    "back":"Resposta"
  }}
]
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        texto = response.text.strip()

        texto = (
            texto.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(texto)

    except Exception as e:
        return {
            "error": str(e)
        }
