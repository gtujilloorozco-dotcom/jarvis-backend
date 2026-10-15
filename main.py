import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai

app = FastAPI()

# Inicializar el cliente de Google GenAI con la API Key configurada en Render
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Modelo de datos que coincide exactamente con Android
class PromptRequest(BaseModel):
    prompt: str

@app.post("/chat")
def chat_with_jarvis(request: PromptRequest):
    # Lista de modelos con estrategia de respaldo (fallback)
    models_to_try = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash"
    ]
    
    last_error = None
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=request.prompt
            )
            # Devuelve el formato que espera JarvisResponse (reply)
            return {"reply": response.text}
        except Exception as e:
            last_error = e
            continue
            
    raise HTTPException(
        status_code=500, 
        detail=f"No se pudo procesar la solicitud con ningún modelo: {str(last_error)}"
    )

@app.get("/")
def home():
    return {"status": "Jarvis backend online"}
