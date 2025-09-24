from flask import Flask, request, send_from_directory
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import threading
import logging
import os

TOKEN = "ВАШ_ТОКЕН_БОТА"

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Отдаём Mini App HTML
@app.route('/')
def index():
    return send_from_directory('miniapp', 'index.html')

# Получаем заявки из Mini App
@app.route('/webapp', methods=['POST'])
def webapp_data():
    data = request.json
    print("Новая заявка:", data)
    return {"status": "ok"}

# Telegram бот
bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("Открыть Mini App", web_app={"url": "http://localhost:5000/"})]]
    update.message.reply_text("Добро пожаловать!", reply_markup=InlineKeyboardMarkup(keyboard))

dispatcher.add_handler(CommandHandler("start", start))

def run_bot():
    updater.start_polling()
    updater.idle()

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(port=5000)