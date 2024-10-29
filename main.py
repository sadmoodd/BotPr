import telebot
from data import token
from telebot import types

bot = telebot.TeleBot(token.__token)

# cool

@bot.message_handler(commands=["start", "help"])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Выбери действие:")
    main_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu_button = types.KeyboardButton("Главное меню")
    main_menu_markup.add(main_menu_button)
    bot.send_message(message.chat.id, "Добро пожаловать! Нажмите на кнопку ниже.", reply_markup=main_menu_markup)



@bot.message_handler(func=lambda message: message.text == "Главное меню")
def show_inline_menu(message):
    inline_menu_markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Кнопка 1", callback_data="button1")
    button2 = types.InlineKeyboardButton("Кнопка 2", callback_data="button2")
    inline_menu_markup.add(button1, button2)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=inline_menu_markup)

@bot.message_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "button1":
        bot.send_message(call.chat.id, "Вы нажали на кнопку 1")
    elif call.data == "button2":
        bot.send_message(call.chat.id, "Вы нажали на кнопку 2")
if __name__ == "__main__":
    bot.infinity_polling()