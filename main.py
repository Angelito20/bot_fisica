from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Bot activo ✅"}

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    print(data)
    return {"ok": True}
