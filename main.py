import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

# Configurar la API key desde las variables de entorno de Render
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

class PromptRequest(BaseModel):
    prompt: str

@app.post("/chat")
def chat_with_jarvis(request: PromptRequest):
    try:
        # Usar el modelo estándar general
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(request.prompt)
        return {"reply": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"status": "Jarvis backend online"}
