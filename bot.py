import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from google import genai

# ========= CONFIG =========
TELEGRAM_TOKEN = "8547596816:AAEBVBLGXXNowDnx7TBY2ZZjV2U9K44Iye0"
GEMINI_API_KEY = "AIzaSyAuJi4T_sPKC4Z3j7hQ42v5ij17mn4nWQs"

# ========= LOG =========
logging.basicConfig(level=logging.INFO)

# ========= GEMINI CLIENT =========
client = genai.Client(api_key=GEMINI_API_KEY)

# ========= BOT LOGIC =========
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    prompt = (
        "Responde como profesor de física, de forma corta y clara. "
        "No uses símbolos raros ni fórmulas con signos especiales. "
        "Si es un test, crea preguntas tipo opción múltiple.\n\n"
        f"Pregunta del alumno: {user_text}"
    )

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        if not response or not response.text:
            await update.message.reply_text("No pude generar la respuesta, intenta otra vez.")
            return

        await update.message.reply_text(response.text)

    except Exception as e:
        logging.error(e)
        await update.message.reply_text("Error al generar respuesta.")

# ========= MAIN =========
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    print("🤖 Bot de Física activo...")
    app.run_polling()

if __name__ == "__main__":
    main()
