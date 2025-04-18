import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from TikTokEditor import TikTokEditor

# Конфигурация
TOKEN = os.getenv("TOKEN")
PORT = int(os.getenv("PORT", 8000))
WEBHOOK_URL = "https://ttbot-z8tk.onrender.com"
OUTPUT_DIR = os.path.abspath("result")
TEMP_DIR = os.path.abspath("temp")

# Инициализация
editor = TikTokEditor()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, _):
    await update.message.reply_text("🎥 Отправьте видео для обработки!")

async def process_video(update: Update, _):
    try:
        # Создаем временные папки
        os.makedirs(TEMP_DIR, exist_ok=True)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Скачивание видео
        file = await update.message.effective_attachment.get_file()
        input_path = os.path.join(TEMP_DIR, f"temp_{update.message.id}.mp4")
        await file.download_to_drive(input_path)

        # Обработка
        output_path = editor.process_video(input_path, OUTPUT_DIR)
        
        if output_path and os.path.exists(output_path):
            # Отправка результата
            await update.message.reply_video(video=open(output_path, "rb"))
            
            # Очистка
            os.remove(input_path)
            os.remove(output_path)
        else:
            await update.message.reply_text("😢 Не удалось обработать видео")

    except Exception as e:
        logging.error(f"Ошибка: {str(e)}", exc_info=True)
        await update.message.reply_text("⚠️ Произошла внутренняя ошибка")

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, process_video))
    
    # Вебхук
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        secret_token=os.getenv("RENDER_SECRET")
    )