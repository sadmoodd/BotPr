import telebot
from data import token

bot = telebot.TeleBot(token.__token)

# cool

@bot.message_handler()
def echo(message):
    bot.send_message(message.chat.id, message.text)

bot.infinity_polling()