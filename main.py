import os
from flask import Flask, request
import telebot
import stripe

# Инициализация
API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)
stripe.api_key = STRIPE_SECRET_KEY

# Пример: команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать в SeZI! Напишите, что хотите заказать.")

# Webhook обработчик
@app.route(f"/{API_TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

# Точка входа Flask
@app.route("/", methods=["GET"])
def index():
    return "SeZI Bot is running!"

if __name__ == "__main__":
    app.run()
