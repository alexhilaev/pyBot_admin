import telebot;
from telebot import types
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type

SECRET_KEY=str(sys.argv[1])
bot = telebot.TeleBot(SECRET_KEY);

users = {}
# @bot.message_handler(content_types=['text'])
# def start(message):
#     if message.text == '/start':
#         bot.send_message(message.from_user.id, "Выберите тему:");
#         bot.register_next_step_handler(message, message_handler); #следующий шаг – функция get_name
#     else:
#         bot.send_message(message.from_user.id, 'Напишите /start');

# def message_handler(message):

@bot.message_handler(content_types=['text'])
def start(message):
    chat_id = message.chat.id
    if message.text == '/start':
        bot.send_message(chat_id, "Выберите тему:");
        keyboard = telebot.types.InlineKeyboardMarkup()
        button0 = telebot.types.InlineKeyboardButton(text="ЖКХ", callback_data='GKH')
        button1 = telebot.types.InlineKeyboardButton(text="Транспорт", callback_data='Transport')
        button2 = telebot.types.InlineKeyboardButton(text="Все разворовали!", callback_data='2')
        button3 = telebot.types.InlineKeyboardButton(text="Disable", callback_data='disable')
        keyboard.add(button0, button1, button2, button3)
        bot.send_message(chat_id,
                     'Добро пожаловать в бота выбора темы',
                     reply_markup=keyboard)
        # bot.register_next_step_handler(message, menu_handler); #следующий шаг – функция get_name
    else:
        bot.send_message(chat_id, 'Напишите /start');


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id  
    if call.data == "GKH": #call.data это callback_data, которую мы указали при объявлении кнопки
        ... #код сохранения данных, или их обработки
        bot.send_message(chat_id, 'ЖКХ!:)');
    elif call.data == "Transport":
        bot.send_message(chat_id, 'ТРАНСПОРТ!:)');
    elif call.data == "2":
        bot.send_message(chat_id, 'Как тяжко жить!:)');
        user_data(message)
    elif call.data == "disable":
        bot.send_message(chat_id, 'menu disabled!');
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, 
                         text='disable!')
        
def user_data(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Введи своё имя')
    users[chat_id] = {}
    bot.register_next_step_handler(message, save_username)
    
def save_username(message):
    chat_id = message.chat.id
    name = message.text
    users[chat_id]['name'] = name
    bot.send_message(chat_id, f'Отлично, {name}. Теперь укажи свою фамилию')
    bot.register_next_step_handler(message, save_surname)

def save_surname(message):
    chat_id = message.chat.id
    surname = message.text
    name = users[chat_id]['name']
    users[chat_id]['surname'] = surname
    surname = users[chat_id]['name']
    bot.send_message(chat_id, f'Отлично, {name} {surname}. Теперь укажи свою почту')
    bot.register_next_step_handler(message, save_email)

def save_email(message):
    chat_id = message.chat.id
    email = message.text
    name = users[chat_id]['name']
    surname = users[chat_id]['surname']
    users[chat_id]['email'] = email
    bot.send_message(chat_id, f'Отлично, {name} {surname}. Твоя почта {email}. Теперь укажи свой телефон в формате 79991234567')
    bot.register_next_step_handler(message, save_phone)
    
def save_phone(message):
    chat_id = message.chat.id
    phone = message.text
    name = users[chat_id]['name']
    users[chat_id]['phone'] = phone
    surname = users[chat_id]['surname']
    if phone[1:].isdigit():
        # bot.send_message(chat_id, f'Отлично, {name} {surname}. {phone} phone check')
        try: 
            carrier._is_mobile(number_type(phonenumbers.parse(phone)))
        except:
            bot.send_message(chat_id, f'Слышь, {name} {surname}, {phone} exception!!')
            bot.register_next_step_handler(message, save_phone)
        else:
            bot.send_message(chat_id, f'Отлично, {name} {surname}. {phone} верный! Теперь функция finish')
            finish(message)
    else:
        bot.send_message(chat_id, f'Слышь, {name} {surname}, {phone} - херня, давай заново!!')
        bot.register_next_step_handler(message, save_phone)


def finish(message):
    chat_id = message.chat.id
    name = users[chat_id]['name']
    surname = users[chat_id]['surname']
    bot.send_message(chat_id, f'Отлично, {name} {surname}, chatid={chat_id}')
    bot.send_message(970499674, f'Отлично, {name} {surname}, chatid={chat_id}')
    bot.send_message(1632618194, f'Отлично, {name} {surname}, chatid={chat_id}')
    # bot.forward_message(chat_id='@nrzx3', from_chat_id=chat_id, message_id=message.id)
    # bot.register_next_step_handler(message, save_surname)

bot.polling(non_stop=True, interval=1)

# def get_name(message): #получаем фамилию
#     global name;
#     name = message.text;
#     bot.send_message(message.from_user.id, 'Какая у тебя фамилия?');
#     bot.register_next_step_handler(message, get_surname);

# def get_surname(message):
#     global surname;
#     surname = message.text;
#     bot.send_message(message.from_user.id, 'Сколько тебе лет?');
#     bot.register_next_step_handler(message, get_age);

# def get_age(message):
#     global age;
#     while age == 0: #проверяем что возраст изменился
#         try:
#              age = int(message.text) #проверяем, что возраст введен корректно
#         except Exception:
#              bot.send_message(message.from_user.id, 'Цифрами, пожалуйста');
