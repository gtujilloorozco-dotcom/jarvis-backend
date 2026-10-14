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
        # Probamos con el modelo estándar de la nueva SDK de Google GenAI
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Responde de forma concisa, elegante y profesional como J.A.R.V.I.S. de Iron Man: {request.prompt}"
        )
        return {"reply": response.text}
    except Exception as e:
        # Si falla, intentamos listar un modelo compatible o devolvemos el error exacto legible
        try:
            # Fallback automático al primer modelo disponible que soporte generación de contenido
            models = client.models.list()
            available_model = "gemini-1.5-flash"
            for m in models:
                if "flash" in m.name:
                    available_model = m.name
                    break
            
            response = client.models.generate_content(
                model=available_model,
                contents=f"Responde de forma concisa, elegante y profesional como J.A.R.V.I.S. de Iron Man: {request.prompt}"
            )
            return {"reply": response.text}
        except Exception as inner_e:
            raise HTTPException(status_code=500, detail=f"Error principal: {str(e)} | Fallback error: {str(inner_e)}")
