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
            model="gemini-2.5-flash",
            contents=f"Responde de forma concisa, elegante y profesional como J.A.R.V.I.S. de Iron Man: {request.prompt}"
        )
        return {"reply": response.text}
    except Exception as e:
        return {"reply": f"EXCEPCIÓN INTERNA: {str(e)}"}
