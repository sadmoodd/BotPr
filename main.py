import telebot
from data import token
from telebot import types
from telebot.types import InputFile
from collections import defaultdict
import os


class Table:
    def __init__(self, name, path_to_photo):
        self.name = name
        self.path = path_to_photo + ".jpg"


# Словарь для хранения учетных данных администраторов
ADMINS = {
    'admin': 'admin123',
    'user': 'pass123'
}

# Словарь для хранения состояния пользователей
user_states = defaultdict(lambda: {'state': None, 'login': None, 'is_admin': False})

# Множество для хранения chat_id всех пользователей
all_users = set()

bot = telebot.TeleBot(token.__token)


@bot.message_handler(commands=["start"])
def start_message(message):
    # Добавляем пользователя в список всех пользователей
    all_users.add(message.chat.id)

    # Создаем клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu_button = types.KeyboardButton("Главное меню")
    authorization_button = types.KeyboardButton("Авторизироваться")

    # Добавляем кнопку отправки сообщения, если пользователь админ
    if user_states[message.chat.id].get('is_admin'):
        send_message_button = types.KeyboardButton("Отправить общее сообщение")
        markup.add(main_menu_button, authorization_button, send_message_button)
    else:
        markup.add(main_menu_button, authorization_button)

    bot.send_message(message.chat.id, "Добро пожаловать в Timetable!", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Авторизироваться")
def auth_callback(message):
    if user_states[message.chat.id].get('is_admin'):
        bot.send_message(message.chat.id, "Вы уже авторизованы как администратор!")
        return

    user_states[message.chat.id]['state'] = 'waiting_login'
    bot.send_message(message.chat.id, "Введите логин:")


@bot.message_handler(func=lambda message: user_states[message.chat.id]['state'] == 'waiting_login')
def handle_login(message):
    user_states[message.chat.id]['login'] = message.text
    user_states[message.chat.id]['state'] = 'waiting_password'
    bot.send_message(message.chat.id, "Введите пароль:")


@bot.message_handler(func=lambda message: user_states[message.chat.id]['state'] == 'waiting_password')
def handle_password(message):
    login = user_states[message.chat.id]['login']
    password = message.text


    if login in ADMINS and ADMINS[login] == password:
        user_states[message.chat.id]['is_admin'] = True
        user_states[message.chat.id]['state'] = None

        # Обновляем клавиатуру с новой кнопкой
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Главное меню"))
        markup.add(types.KeyboardButton("Авторизироваться"))
        markup.add(types.KeyboardButton("Отправить общее сообщение"))

        bot.send_message(message.chat.id, "✅ Авторизация успешна! Теперь вы можете отправлять общие сообщения.",
                         reply_markup=markup)
    else:
        user_states[message.chat.id]['state'] = None
        user_states[message.chat.id]['is_admin'] = False
        bot.send_message(message.chat.id, "❌ Неверный логин или пароль. Попробуйте авторизоваться снова.")


@bot.message_handler(func=lambda message: message.text == "Отправить общее сообщение")
def request_broadcast_message(message):
    if not user_states[message.chat.id].get('is_admin'):
        bot.send_message(message.chat.id, "У вас нет прав для отправки общих сообщений!")
        return

    user_states[message.chat.id]['state'] = 'waiting_broadcast'
    bot.send_message(message.chat.id, "Введите сообщение для рассылки:")


@bot.message_handler(func=lambda message: user_states[message.chat.id]['state'] == 'waiting_broadcast')
def send_broadcast(message):
    if not user_states[message.chat.id].get('is_admin'):
        return

    broadcast_message = message.text
    failed_sends = 0

    for user_id in all_users:
        try:
            bot.send_message(user_id, f"📢 Объявление:\n\n{broadcast_message}")
        except Exception:
            failed_sends += 1

    user_states[message.chat.id]['state'] = None
    bot.send_message(message.chat.id,
                     f"✅ Сообщение отправлено!\nУспешно: {len(all_users) - failed_sends}\nНе доставлено: {failed_sends}")


@bot.message_handler(func=lambda message: message.text == "Главное меню")
def show_inline_menu(message):
    inline_menu_markup = types.InlineKeyboardMarkup(row_width=2)  # Устанавливаем ширину строки
    buttons = []

    for i in range(1, 6):
        buttons.append(types.InlineKeyboardButton(f"{i} курс", callback_data=f"{i} курс"))

    for i in range(0, len(buttons), 2):
        row = buttons[i:min(i + 2, len(buttons))]
        inline_menu_markup.row(*row)

    bot.send_message(message.chat.id, "Выберите курс:", reply_markup=inline_menu_markup)


@bot.callback_query_handler(func=lambda call: call.data.endswith("курс"))
def callback_query(call):
    selected_course = call.data
    bot.answer_callback_query(call.id, f"Вы выбрали {selected_course}")

    course_groups = {
        '1 курс': ["ИТ-0110224", "ИТ-0930224", "ИТ-0940324", "ИТ-1035224",
                   "ИТ-1320124", "ИТ-1540124", "ИТ-2740224", "ИТ-4451124"],
        '2 курс': ["ИТ-0110223", "ИТ-0115323", "ИТ-0320123", "ИТ-0930323",
                   "ИТ-0930223", "ИТ-1035223", "ИТ-1320123", "ИТ-1540123",
                   "ИТ-2740223", "ИТ-4450523"],
        '3 курс': ["ИТ-0110222", "ИТ-0115322", "ИТ-0320122", "ИТ-0930222",
                   "ИТ-0940322", "ИТ-1035222", "ИТ-1320122", "ИТ-1540122",
                   "ИТ-2740122", "ИТ-4450522"],
        '4 курс': ["ИТ-0110221", "ИТ-0115321", "ИТ-0930221", "ИТ-0940321",
                   "ИТ-1035221", "ИТ-1320121", "ИТ-1540121", "ИТ-2740121",
                   "ИТ-4450521"],
        '5 курс': ["ИТ-1035120", "ИТ-4450520"]
    }

    if selected_course in course_groups:
        inline_menu_markup = types.InlineKeyboardMarkup(row_width=3)
        groups = course_groups[selected_course]
        buttons = []

        for group in groups:
            buttons.append(types.InlineKeyboardButton(group, callback_data=group))

        for i in range(0, len(buttons), 3):
            row = buttons[i:min(i + 3, len(buttons))]
            inline_menu_markup.row(*row)

        bot.send_message(call.message.chat.id, "Выберите группу:", reply_markup=inline_menu_markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if not call.data.endswith("курс"):
        send_choice(call.message.chat.id, call.data)
        try:

            # Получаем абсолютный путь к директории проекта
            project_path = os.path.abspath(os.path.dirname(__file__))

            # Формируем путь к директории data
            data_path = os.path.join(project_path, 'data')

            image = Table(call.data, rf'{data_path}\{call.data}\{call.data}')
            photo = InputFile(image.path)
            bot.send_photo(call.message.chat.id, photo=photo)
        except Exception:
            bot.send_message(call.message.chat.id, "Произошла ошибка при загрузке расписания.")


def send_choice(chat_id, group_name):
    bot.send_message(chat_id, f"Вы выбрали группу {group_name}")


if __name__ == "__main__":
    bot.infinity_polling()
