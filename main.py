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
    MODEL_NAME = "gemini-3.8-flash"
    
    # Configuramos reintentos para superar los picos de saturación (503)
    max_retries = 6
    delay = 3.0  
    
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
            if "503" in last_error or "UNAVAILABLE" in last_error or "high demand" in last_error:
                time.sleep(delay)
                delay *= 1.5  # Espera progresiva entre intentos
                continue
            else:
                break

    raise HTTPException(status_code=500, detail=f"Servidores saturados temporalmente (503). Vuelve a pulsar Execute en unos segundos. Detalle: {last_error}")
