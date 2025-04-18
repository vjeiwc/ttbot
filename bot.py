import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from TikTokEditor import TikTokEditor

# Конфигурация (ЗАМЕНИТЕ НАСТРОЙКИ)
TOKEN = os.getenv("TOKEN")  # Токен из переменных окружения Render
WEBHOOK_URL = "https://ttbot-z8tk.onrender.com"  # Ваш URL
PORT = int(os.getenv("PORT", 8000))
OUTPUT_DIR = os.path.abspath("result")
TEMP_DIR = os.path.abspath("temp")

# Инициализация
editor = TikTokEditor()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

async def start(update: Update, _):
    """Обработчик команды /start"""
    try:
        await update.message.reply_text("🎥 Отправьте видео для обработки (до 20MB)!")
        logging.info("Пользователь %s вызвал /start", update.effective_user.id)
    except Exception as e:
        logging.error("Ошибка в /start: %s", e)

async def process_video(update: Update, _):
    """Обработчик видео"""
    input_path = output_path = None
    try:
        file = await update.message.effective_attachment.get_file()
        input_path = os.path.join(TEMP_DIR, f"temp_{update.message.id}.mp4")
        await file.download_to_drive(input_path)
        
        output_path = editor.process_video(input_path, OUTPUT_DIR)
        
        if output_path:
            await update.message.reply_video(
                video=open(output_path, "rb"),
                caption="✅ Видео обработано!"
            )
        else:
            await update.message.reply_text("❌ Ошибка обработки")

    except Exception as e:
        logging.error("Ошибка: %s", e, exc_info=True)
        await update.message.reply_text("⚠️ Произошла ошибка")
    finally:
        # Удаление временных файлов
        for path in [input_path, output_path]:
            if path and os.path.exists(path):
                os.remove(path)

if __name__ == "__main__":
    # Создаем папки
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Инициализация бота
    app = Application.builder().token(TOKEN).build()
    
    # Регистрация обработчиков
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, process_video))

    # Запуск вебхука
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        secret_token=os.getenv("RENDER_SECRET"),  # Секрет из переменных Render
        drop_pending_updates=True
    )