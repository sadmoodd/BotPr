import telebot
from data import token
from telebot import types
from telebot.types import InputFile


class Table:
    def __init__(self, name, path_to_photo):
        self.name = name
        self.path = path_to_photo + ".jpg"


bot = telebot.TeleBot(token.__token)


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
    for i in range(1, 6):
        button = types.InlineKeyboardButton(f"{i} курс", callback_data=f"{i} курс")
        inline_menu_markup.add(button)
    bot.send_message(message.chat.id, "Выберите курс:", reply_markup=inline_menu_markup)


@bot.callback_query_handler(func=lambda call: call.data.endswith("курс"))
def callback_query(call):
    if call.message:
        selected_course = call.data
        bot.answer_callback_query(call.id, f"Вы выбрали {selected_course}")

        if selected_course == '1 курс':
            inline_menu_markup = types.InlineKeyboardMarkup()
            courses = [
                "ИТ-0110224",
                "ИТ-0930224",
                "ИТ-0940324",
                "ИТ-1035224",
                "ИТ-1320124",
                "ИТ-1540124",
                "ИТ-2740224",
                "ИТ-4451124"
            ]
            for course in courses:
                button = types.InlineKeyboardButton(course, callback_data=course)
                inline_menu_markup.add(button)
            bot.send_message(call.message.chat.id, "Выберите группу:", reply_markup=inline_menu_markup)

        elif selected_course == '2 курс':
            inline_menu_markup = types.InlineKeyboardMarkup()
            courses = [
                "ИТ-0110223",
                "ИТ-0115323",
                "ИТ-0320123",
                "ИТ-0930323",
                "ИТ-0940223",
                "ИТ-1035223",
                "ИТ-1320123",
                "ИТ-1540123",
                "ИТ-2740223",
                "ИТ-4450523"
            ]
            for course in courses:
                button = types.InlineKeyboardButton(course, callback_data=course)
                inline_menu_markup.add(button)
            bot.send_message(call.message.chat.id, "Выберите группу:", reply_markup=inline_menu_markup)

        elif selected_course == '3 курс':
            inline_menu_markup = types.InlineKeyboardMarkup()
            courses = [
                "ИТ-0110222",
                "ИТ-0115322",
                "ИТ-0320122",
                "ИТ-0930222",
                "ИТ-0940322",
                "ИТ-1035222",
                "ИТ-1320122",
                "ИТ-1540122",
                "ИТ-2740122",
                "ИТ-4450522"
            ]
            for course in courses:
                button = types.InlineKeyboardButton(course, callback_data=course)
                inline_menu_markup.add(button)
            bot.send_message(call.message.chat.id, "Выберите группу:", reply_markup=inline_menu_markup)

        elif selected_course == '4 курс':
            inline_menu_markup = types.InlineKeyboardMarkup()
            courses = [
                "ИТ-0110221",
                "ИТ-0115321",
                "ИТ-0930221",
                "ИТ-0940321",
                "ИТ-1035221",
                "ИТ-1320121",
                "ИТ-1540121",
                "ИТ-2740121",
                "ИТ-4450521"
            ]
            for course in courses:
                button = types.InlineKeyboardButton(course, callback_data=course)
                inline_menu_markup.add(button)
            bot.send_message(call.message.chat.id, "Выберите группу:", reply_markup=inline_menu_markup)

        elif selected_course == '5 курс':
            inline_menu_markup = types.InlineKeyboardMarkup()
            courses = [
                "ИТ-1035120",
                "ИТ-4450520"
            ]
            for course in courses:
                button = types.InlineKeyboardButton(course, callback_data=course)
                inline_menu_markup.add(button)
            bot.send_message(call.message.chat.id, "Выберите группу:", reply_markup=inline_menu_markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    send_choice(call.message.chat.id, call.data)

    image = Table(call.data, rf'C:\Users\Роман\PycharmProjects\BotPr\data\{call.data}\{call.data}')
    photo = InputFile(image.path)

    inline_menu_markup = types.InlineKeyboardMarkup()
    for discipline in disciplines:
        button = types.InlineKeyboardButton(discipline, callback_data=discipline)
        inline_menu_markup.add(button)

    bot.send_photo(call.message.chat.id, photo=photo, reply_markup=keyboard)


def send_choice(chat_id, group_name):
    bot.answer_callback_query(chat_id, f"Вы выбрали {group_name}")


if __name__ == "__main__":
    bot.infinity_polling()
