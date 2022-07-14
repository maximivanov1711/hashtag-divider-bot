import os
import telebot
from flask import Flask, request


TOKEN = '5478875450:AAE-lbtYwOmowKZ5_Ib3V_ZLDRQvlEu60m8'
APP_URL = f'https://hashtag-divider-bot.herokuapp.com/{TOKEN}'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commans=['start'])
def start(message):
    bot.reply_to(message, f'Hello {message.from_user.first_name}')


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo(message):
    lines = message.text.split('#')

    for i in range(1, len(lines), 3):
        bot.reply_to('#' + '#'.join(lines[i: i + 3]))


@server.route(f'/{TOKEN}', methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    
    return '!', 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)

    return '!', 200

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
