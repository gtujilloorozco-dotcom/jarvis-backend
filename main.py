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
    prompt_formatted = f"Responde de forma muy concisa, elegante y directa como J.A.R.V.I.S. de Iron Man: {request.prompt}"
    
    # Modelos rápidos en orden de preferencia
    models_to_try = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-3.8-flash"
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
        "reply": "Señor, los servidores centrales experimentan alta demanda. Reintente en unos instantes."
    }
