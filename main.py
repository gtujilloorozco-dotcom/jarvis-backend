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
    # Usamos modelos estables de la API de Google
    models_to_try = ["gemini-1.5-flash", "gemini-1.5-pro"]
    
    last_error = ""
    for model_name in models_to_try:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=f"Responde de forma concisa, elegante y profesional como J.A.R.V.I.S. de Iron Man: {request.prompt}"
                )
                return {"reply": response.text}
            except Exception as e:
                last_error = str(e)
                if "503" in last_error or "UNAVAILABLE" in last_error:
                    time.sleep(2)
                    continue
                break
                
    raise HTTPException(status_code=500, detail=f"Error al conectar con Jarvis: {last_error}")
