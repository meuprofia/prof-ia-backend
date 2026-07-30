import os
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

app = FastAPI()

# Permite que seu site/landing page converse com esse backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
)

class PromptRequest(BaseModel):
    user_input: str

@app.post("/api/chat")
async def process_prompt(request: PromptRequest):
    try:
        tools = [
            {'type': 'code_execution'},
            {'type': 'google_search'},
            {'type': 'url_context'},
        ]

        interaction = client.interactions.create(
            agent='antigravity-preview-05-2026',
            input=request.user_input,
            background=True,
            tools=tools,
            environment={
                'type': 'remote',
                'network': 'disabled',
            },
        )

        # Aguarda a resposta do modelo
        while True:
            interaction = client.interactions.get(interaction.id)
            if interaction.status == "completed":
                return {"response": interaction.output_text}
            elif interaction.status == "failed":
                raise HTTPException(status_code=500, detail=f"Erro na IA: {interaction.error}")
            time.sleep(2)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
