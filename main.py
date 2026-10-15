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
    
    # Lista de modelos a probar si uno falla por saturación
    models_to_try = ["gemini-2.5-flash", "gemini-3.8-flash", "gemini-1.5-flash"]
    
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt_formatted
            )
            return {"reply": response.text}
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                continue # Prueba con el siguiente modelo si está saturado
            # Si es otro tipo de error, prueba el siguiente modelo
            continue

    # Si todos los modelos están en pico de tráfico
    return {
        "reply": "Señor, los servidores centrales de Google experimentan una alta demanda en este momento. Por favor, reintente la orden en unos segundos."
    }
