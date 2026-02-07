import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters
)

# ====== CONFIG ======
TELEGRAM_TOKEN = os.getenv("8547596816:AAEBVBLGXXNowDnx7TBY2ZZjV2U9K44Iye0")
GEMINI_API_KEY = os.getenv("AIzaSyAuJi4T_sPKC4Z3j7hQ42v5ij17mn4nWQs")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")


# ====== HANDLER ======
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        pregunta = update.message.text
        respuesta = model.generate_content(pregunta)
        await update.message.reply_text(respuesta.text)
    except Exception as e:
        await update.message.reply_text("Ocurrió un error 😕")


# ====== MAIN ======
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, responder)
    )

    print("🤖 Bot activo 24/7...")
    app.run_polling()


if __name__ == "__main__":
    main()
