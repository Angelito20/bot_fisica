import os
import time
import google.generativeai as genai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)

# ======================
# CONFIGURACIÓN
# ======================

TELEGRAM_TOKEN = os.getenv("8547596816:AAEBVBLGXXNowDnx7TBY2ZZjV2U9K44Iye0")
GEMINI_API_KEY = os.getenv("AIzaSyAuJi4T_sPKC4Z3j7hQ42v5ij17mn4nWQs")

if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    raise RuntimeError("Faltan variables de entorno")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Control simple de espera por usuario (anti cuota)
user_last_request = {}
WAIT_SECONDS = 60

# ======================
# FUNCIÓN PRINCIPAL
# ======================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    now = time.time()
    last = user_last_request.get(user_id, 0)

    if now - last < WAIT_SECONDS:
        await update.message.reply_text(
            "⏳ Espera 1 minuto antes de hacer otra pregunta."
        )
        return

    user_last_request[user_id] = now

    try:
        prompt = (
            "Responde de forma corta, clara y sin símbolos raros.\n"
            "Tema: física.\n\n"
            f"Pregunta: {text}"
        )

        response = model.generate_content(prompt)

        answer = response.text.strip()
        await update.message.reply_text(answer)

    except Exception as e:
        error_text = str(e)

        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
            await update.message.reply_text(
                "😓 Estoy recibiendo muchas preguntas.\n"
                "Espera un momento y vuelve a intentar."
            )
        else:
            await update.message.reply_text(
                "❌ Error al generar la respuesta."
            )

# ======================
# ARRANQUE DEL BOT
# ======================

def main():
    print("🤖 Bot de Física activo...")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    app.run_polling()

if __name__ == "__main__":
    main()

      
