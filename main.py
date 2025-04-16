import telebot
from flask import Flask, request

TOKEN = 'ТВОЙ_ТОКЕН_ОТ_БОТА'  # замени на свой токен
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Добро пожаловать в SeZI! Напишите, что хотите купить.")

# Обработка текста (покупка товара)
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text.lower()
    if "айфон" in user_text:
        bot.send_message(message.chat.id, "Айфон есть в наличии! Цена: 999$. Оплатите по ссылке: https://example.com/pay")
    elif "чехол" in user_text:
        bot.send_message(message.chat.id, "Чехлы от 9$. Вот ссылка на оплату: https://example.com/pay")
    else:
        bot.send_message(message.chat.id, "Извините, этого товара нет. Напишите, что вы хотите купить.")

# Webhook для Render
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

# Устанавливаем webhook при запуске
@app.route('/')
def index():
    bot.remove_webhook()
    bot.set_webhook(url=f'https://ТВОЙ_RENDER_URL/{TOKEN}')  # замени на свой Render URL
    return "Webhook установлен!"

if __name__ == "__main__":
    app.run()

