from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

TOKEN = os.getenv("8547596816:AAEBVBLGXXNowDnx7TBY2ZZjV2U9K44Iye0")
API_URL = f"https://api.telegram.org/bot{TOKEN}"

@app.get("/")
async def root():
    return {"status": "OK"}

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print("UPDATE:", data)

    if "message" not in data:
        return {"ok": True}

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "mensaje sin texto")

    r = requests.post(
        f"{API_URL}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": f"✅ Te leí: {text}"
        }
    )

    print("RESPUESTA TELEGRAM:", r.text)
    return {"ok": True}

