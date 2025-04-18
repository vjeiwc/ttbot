import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from TikTokEditor import TikTokEditor

# Получаем токен и порт из переменных окружения
TOKEN = "8024034425:AAGIIRzgZIzeABT2Pzikmc71TDUZFiidtiU"
PORT = int(os.getenv("PORT", 8000))  # 8000 — значение по умолчанию

# Путь для сохранения обработанных видео
OUTPUT_DIR = "result"

# Инициализация редактора
editor = TikTokEditor()

async def start(update: Update, context):
    await update.message.reply_text("Привет! Отправь мне видео, и я его обработаю.")

async def process_video(update: Update, context):
    try:
        # Скачиваем видео
        file = await update.message.effective_attachment.get_file()
        input_path = f"temp_{update.message.message_id}.mp4"
        await file.download_to_drive(input_path)
        
        # Обрабатываем видео
        output_path = editor.process_video(input_path, OUTPUT_DIR)
        
        if output_path:
            # Отправляем обратно обработанное видео
            await update.message.reply_video(video=open(output_path, 'rb'))
            os.remove(input_path)
        else:
            await update.message.reply_text("Ошибка обработки 😢")

    except Exception as e:
        logging.error(str(e))
        await update.message.reply_text("Что-то пошло не так!")

if __name__ == "__main__":
    # Создаем приложение с токеном
    app = Application.builder().token(TOKEN).build()

    # Добавляем обработчики команд и сообщений
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, process_video))

    # Настраиваем вебхук для работы через Render
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url="https://your-app.onrender.com",  # Замените на ваш URL
        secret_token=os.getenv("RENDER_SECRET")
    )
