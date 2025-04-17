import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from TikTokEditor import TikTokEditor

TOKEN = "8024034425:AAGIIRzgZIzeABT2Pzikmc71TDUZFiidtiU"
OUTPUT_DIR = "result"

editor = TikTokEditor()

async def start(update: Update, context):
    await update.message.reply_text("Привет! Отправь мне видео, и я его обработаю.")

async def process_video(update: Update, context):
    try:
        file = await update.message.effective_attachment.get_file()
        input_path = f"temp_{update.message.message_id}.mp4"
        await file.download_to_drive(input_path)
        
        output_path = editor.process_video(input_path, OUTPUT_DIR)
        
        if output_path:
            await update.message.reply_video(video=open(output_path, 'rb'))
            os.remove(input_path)
        else:
            await update.message.reply_text("Ошибка обработки 😢")

    except Exception as e:
        logging.error(str(e))
        await update.message.reply_text("Что-то пошло не так!")

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, process_video))
    app.run_polling()