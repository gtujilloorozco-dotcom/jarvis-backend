import os
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai

app = FastAPI()

# Inicializa el cliente de Gemini leyendo la variable segura de Render
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"status": "Jarvis online y listo."}

@app.post("/chat")
def chat(request: PromptRequest):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Responde de forma concisa, elegante y profesional como J.A.R.V.I.S. de Iron Man: {request.prompt}"
    )
    return {"reply": response.text}
