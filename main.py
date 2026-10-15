import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

# Configurar genai con la clave de entorno
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/chat")
def chat_with_jarvis(request: PromptRequest):
    models_to_try = [
        "gemini-1.5-flash",
        "gemini-2.5-flash",
        "gemini-2.0-flash"
    ]
    
    last_error = None
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(request.prompt)
            return {"reply": response.text}
        except Exception as e:
            last_error = e
            continue
            
    raise HTTPException(
        status_code=500, 
        detail=f"No se pudo procesar la solicitud: {str(last_error)}"
    )

@app.get("/")
def home():
    return {"status": "Jarvis backend online"}
