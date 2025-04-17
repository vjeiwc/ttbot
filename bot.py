import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from TikTokEditor import TikTokEditor

# Конфигурация
TOKEN = "8024034425:AAGIIRzgZIzeABT2Pzikmc71TDUZFiidtiU"
OUTPUT_DIR = os.path.abspath("result")  # Абсолютный путь
MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 50 MB

# Инициализация
editor = TikTokEditor()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, _):
    await update.message.reply_text("🎬 Отправь мне видео, и я обработаю его для TikTok!")

async def process_video(update: Update, _):
    try:
        # Проверка размера видео
        if update.message.video.file_size > MAX_VIDEO_SIZE:
            await update.message.reply_text("❌ Файл слишком большой (макс. 50 МБ)")
            return

        # Скачивание
        file = await update.message.video.get_file()
        input_path = os.path.abspath(f"temp_{update.message.message_id}.mp4")
        await file.download_to_drive(input_path)
        
        # Обработка
        output_path = editor.process_video(input_path, OUTPUT_DIR)
        
        if output_path and os.path.exists(output_path):
            await update.message.reply_video(video=open(output_path, 'rb'))
            os.remove(input_path)  # Чистка временных файлов
        else:
            await update.message.reply_text("😢 Не удалось обработать видео")

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        await update.message.reply_text("⚠️ Произошла ошибка. Попробуйте ещё раз.")

    finally:
        # Удаляем временные файлы, если остались
        if 'input_path' in locals() and os.path.exists(input_path):
            os.remove(input_path)

if __name__ == "__main__":
    # Создаем папку для результатов при запуске
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, process_video))
    
    app.run_polling()
