import os
import time
from fastapi import FastAPI, HTTPException
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
    # Modelos válidos y actuales del SDK de Google GenAI
    models_to_try = ["gemini-2.0-flash", "gemini-2.5-flash"]
    
    last_error = ""
    for model_name in models_to_try:
        # Reintentamos hasta 4 veces por modelo si hay picos de demanda
        for attempt in range(4):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=f"Responde de forma concisa, elegante y profesional como J.A.R.V.I.S. de Iron Man: {request.prompt}"
                )
                return {"reply": response.text}
            except Exception as e:
                last_error = str(e)
                # Si hay pico de demanda (503), esperamos un poco y reintentamos
                if "503" in last_error or "UNAVAILABLE" in last_error or "high demand" in last_error:
                    time.sleep(1.5)
                    continue
                # Si es otro error (por ejemplo modelo no encontrado), pasamos al siguiente modelo
                break
                
    raise HTTPException(status_code=500, detail=f"Error en el servicio de Gemini: {last_error}")
