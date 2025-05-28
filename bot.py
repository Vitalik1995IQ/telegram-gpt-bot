import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import openai
from gtts import gTTS
from pydub import AudioSegment

# Загрузка токенов из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await context.bot.get_file(update.message.voice.file_id)
    file_path = await file.download_to_drive()
    # Здесь можно вставить вызов Whisper для распознавания речи (упрощено)
    recognized_text = "Пример распознанного текста"  # Заменить на распознавание
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": recognized_text}]
    )
    answer = response.choices[0].message.content
    tts = gTTS(answer, lang="ru")
    tts.save("response.mp3")
    audio = AudioSegment.from_mp3("response.mp3")
    audio.export("response.ogg", format="ogg")
    await update.message.reply_voice(voice=open("response.ogg", "rb"))

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.VOICE, handle_voice))
app.run_polling()
if name == 'main':
    print("Bot started successfully")
    app.run_polling()
