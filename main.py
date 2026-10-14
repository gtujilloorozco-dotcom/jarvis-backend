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
    max_retries = 3
    delay = 2
    
    last_error = None
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=f"Responde de forma concisa, elegante y profesional como J.A.R.V.I.S. de Iron Man: {request.prompt}"
            )
            return {"reply": response.text}
        except Exception as e:
            last_error = str(e)
            # Si hay alta demanda u otro error temporal, esperamos y reintentamos
            if "503" in last_error or "UNAVAILABLE" in last_error:
                time.sleep(delay)
                delay *= 2
                continue
            else:
                break
                
    raise HTTPException(status_code=500, detail=last_error)
