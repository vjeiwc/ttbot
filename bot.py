import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from TikTokEditor import TikTokEditor

# Конфигурация
TOKEN = os.getenv("TOKEN")
PORT = int(os.getenv("PORT", 8000))
WEBHOOK_URL = "https://your-app.onrender.com"
OUTPUT_DIR = os.path.abspath("result")
TEMP_DIR = os.path.abspath("temp")

# Инициализация
editor = TikTokEditor()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log", mode="w", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

async def start(update: Update, _):
    await update.message.reply_text("🎬 Отправьте видео до 20MB и 55 секунд")

async def cleanup_files(*paths):
    for path in paths:
        try:
            if path and os.path.exists(path):
                os.remove(path)
        except Exception as e:
            logging.error("Ошибка удаления %s: %s", path, e)

async def process_video(update: Update, _):
    input_path = output_path = None
    try:
        # Скачивание
        file = await update.message.effective_attachment.get_file()
        input_path = os.path.join(TEMP_DIR, f"temp_{update.message.id}.mp4")
        await file.download_to_drive(input_path)
        
        # Обработка
        output_path = editor.process_video(input_path, OUTPUT_DIR)
        
        if output_path:
            await update.message.reply_video(
                video=open(output_path, "rb"),
                caption="✅ Готово!",
                write_timeout=30
            )
            
    except Exception as e:
        logging.error("Ошибка обработки: %s", e)
        await update.message.reply_text("🚫 Не удалось обработать видео")
        
    finally:
        await cleanup_files(input_path, output_path)

if __name__ == "__main__":
    try:
        # Проверка директорий
        os.makedirs(TEMP_DIR, exist_ok=True)
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.VIDEO, process_video))
        
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=WEBHOOK_URL,
            secret_token=os.getenv("RENDER_SECRET"),
            drop_pending_updates=True
        )
    except Exception as e:
        logging.critical("Критическая ошибка: %s", e)
