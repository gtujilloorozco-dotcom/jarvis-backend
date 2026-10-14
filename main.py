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
    # Modelo oficial y activo requerido por la API
    MODEL_NAME = "gemini-3.8-flash"
    
    max_retries = 5
    delay = 2.0  # segundos de espera inicial si hay alta demanda
    
    last_error = ""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=f"Responde de forma concisa, elegante y profesional como J.A.R.V.I.S. de Iron Man: {request.prompt}"
            )
            return {"reply": response.text}
        except Exception as e:
            last_error = str(e)
            # Si hay alta demanda / saturacion temporal (503), esperamos y reintentamos automáticamente
            if "503" in last_error or "UNAVAILABLE" in last_error or "high demand" in last_error:
                time.sleep(delay)
                delay *= 1.5  # Incrementa ligeramente el tiempo entre intentos
                continue
            else:
                # Si es un error distinto, rompe el bucle para mostrarlo
                break

    raise HTTPException(status_code=500, detail=f"Error al conectar con Jarvis: {last_error}")
