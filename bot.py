import os
from fastapi import FastAPI
from google import genai

# Leer variables de entorno
API_KEY = os.getenv("GEMINI_API_KEY")
PORT = int(os.getenv("PORT", 8000))

if not API_KEY:
    raise RuntimeError("Faltan variables de entorno")

# Configurar Gemini
client = genai.Client(api_key=API_KEY)

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Bot funcionando correctamente 🚀"}

@app.get("/ask")
def ask(prompt: str):
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )
    return {"response": response.text}

# Para Railway
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
