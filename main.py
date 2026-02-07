from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

TOKEN = os.getenv("8547596816:AAEBVBLGXXNowDnx7TBY2ZZjV2U9K44Iye0")
API_URL = f"https://api.telegram.org/bot{8547596816:AAEBVBLGXXNowDnx7TBY2ZZjV2U9K44Iye0}"

@app.get("/")
def root():
    return {"status": "Bot funcionando 🚀"}

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print("MENSAJE:", data)

    if "message" not in data:
        return {"ok": True}

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")

    requests.post(
        f"{API_URL}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": f"✅ Te leí: {text}"
        }
    )

    return {"ok": True}
