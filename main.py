import os
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai

app = FastAPI()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"status": "Jarvis online y listo."}

@app.post("/chat")
def chat(request: PromptRequest):
    prompt_formatted = f"Responde de forma concisa, elegante y profesional como J.A.R.V.I.S. de Iron Man: {request.prompt}"
    
    # Nombres de modelos actualizados para la API actual
    models_to_try = [
        "gemini-3.8-flash",
        "gemini-2.5-flash",
        "gemini-flash",
        "gemini-2.0-flash"
    ]
    
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt_formatted
            )
            if response and response.text:
                return {"reply": response.text}
        except Exception:
            continue

    return {
        "reply": "Señor, los servidores centrales de Google experimentan alta demanda en este instante. Por favor, reintente en unos segundos."
    }
