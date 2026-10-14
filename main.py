import os
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
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=f"Responde de forma concisa, elegante y profesional como J.A.R.V.I.S. de Iron Man: {request.prompt}"
        )
        return {"reply": response.text}
    except Exception as e:
        error_str = str(e)
        if "503" in error_str or "UNAVAILABLE" in error_str or "high demand" in error_str:
            # Respuesta elegante simulando el estilo de Jarvis cuando hay saturación
            return {
                "reply": "Señor, los servidores centrales experimentan un pico de tráfico temporal. Por favor, reintente en unos instantes."
            }
        raise HTTPException(status_code=500, detail=error_str)
