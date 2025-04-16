import os
from flask import Flask, request
import telebot
import stripe
import requests

# Инициализация
API_TOKEN = os.getenv("API_TOKEN")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Новый параметр

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)
stripe.api_key = STRIPE_SECRET_KEY

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать в SeZI! Напишите, что хотите купить.")

# Обработка Webhook от Telegram
@app.route(f"/{API_TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

# Проверка сервера
@app.route("/", methods=['GET'])
def index():
    return "SeZI Bot is running!"

# Установка Webhook
@app.before_first_request
def set_webhook():
    url = f"https://api.telegram.org/bot{API_TOKEN}/setWebhook"
    data = {"url": f"{WEBHOOK_URL}/{API_TOKEN}"}
    response = requests.post(url, data=data)
    print("Webhook set:", response.text)

if __name__ == "__main__":
    app.run()
