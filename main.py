import telebot
from data import token
from telebot import types


class Table:
    def __init__(self, name, path_to_photo):
        self.name = name
        self.path = path_to_photo + ".jpg"



bot = telebot.TeleBot(token.__token)
# cool

@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Выбери действие:")
    main_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu_button = types.KeyboardButton("Главное меню")
    main_menu_markup.add(main_menu_button)
    bot.send_message(message.chat.id, "Добро пожаловать в Timetable! Нажмите на кнопку ниже.", reply_markup=main_menu_markup)



@bot.message_handler(func=lambda message: message.text == "Главное меню")
def show_inline_menu(message):
    inline_menu_markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("ИТ-0930223", callback_data="ИТ-0930223")
    inline_menu_markup.add(button1)
    bot.send_message(message.chat.id, "Выберите группу:", reply_markup=inline_menu_markup)



@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'ИТ-0930223':
        send_choice(call.message.chat.id, call.data)
        eval(f'from {call.data} import data')
        group = Table(call.data, )


def send_choice(chat_id, group_name):
    bot.send_message(chat_id, f"Вы выбрали группу {group_name}")

if __name__ == "__main__":
    bot.infinity_polling()