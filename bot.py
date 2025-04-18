import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from TikTokEditor import TikTokEditor

TOKEN = os.getenv("TOKEN")
PORT = int(os.getenv("PORT", 8000))
WEBHOOK_URL = "https://ttbot-z8tk.onrender.com"
OUTPUT_DIR = os.path.abspath("result")

editor = TikTokEditor()
logging.basicConfig(level=logging.INFO)

async def start(update: Update, _):
    await update.message.reply_text("🎬 Отправьте видео для обработки")

async def process_video(update: Update, _):
    try:
        file = await update.message.effective_attachment.get_file()
        input_path = f"temp_{update.message.id}.mp4"
        await file.download_to_drive(input_path)
        
        output_path = editor.process_video(input_path, OUTPUT_DIR)
        
        if output_path and os.path.exists(output_path):
            await update.message.reply_video(video=open(output_path, "rb"))
            os.remove(input_path)
            os.remove(output_path)
        else:
            await update.message.reply_text("❌ Ошибка обработки")

    except Exception as e:
        logging.error(f"Ошибка: {str(e)}")
        await update.message.reply_text("⚠️ Произошла ошибка")

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, process_video))
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        secret_token=os.getenv("RENDER_SECRET")
    )
