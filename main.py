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
    # Lista de modelos ordenados por preferencia
    models_to_try = ["gemini-3.8-flash", "gemini-2.5-flash", "gemini-1.5-flash"]
    
    last_error = ""
    for model_name in models_to_try:
        # Reintentamos hasta 2 veces por modelo en caso de picos repentinos
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=f"Responde de forma concisa, elegante y profesional como J.A.R.V.I.S. de Iron Man: {request.prompt}"
                )
                return {"reply": response.text}
            except Exception as e:
                last_error = str(e)
                if "503" in last_error or "UNAVAILABLE" in last_error:
                    time.sleep(1)
                    continue
                break # Si es otro tipo de error, pasa al siguiente modelo
                
    raise HTTPException(status_code=500, detail=f"Todos los modelos fallaron. Último error: {last_error}")
