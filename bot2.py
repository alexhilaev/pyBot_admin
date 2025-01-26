import telebot;
from telebot import types
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
import json
import os.path
import sys


SECRET_KEY=str(sys.argv[1])
bot = telebot.TeleBot(SECRET_KEY);

user = {}
users = {}
admin = {}
adminList = {}
adminThemesList = []
userList = [dict() for x in range(0)]
button = {}
themes = ["ЖКХ", "Транспорт", "Образование"]
admin_btn = ["Регистрация", 
             "Просмотр открытых обращений согласно темам", 
             "Просмотр открытых обращений", 
             "Просмотр всех обращений", 
             "Ответить"]
admin_btn_callback = ["register", 
                      "appeal_themes_wiew", 
                      "appeal_opened_view", 
                      "appeal_all_view", 
                      "reply"]
selTheme = 0
appealNum = 0
userMode = 0
themeReg = 0

welcome = ['Приветствуем в боте регистрации заявок, вы можете подать заявку. Для этого нужно оставить сове ФИО, Электронную почту, телефон и текст заявки.']

@bot.message_handler(content_types=['text'])
def start(message):
    chat_id = message.chat.id
    if message.text == '/start':
        user_branch(message)
    elif message.text == '/admin':
        admin_branch(message)
    elif message.text == '/superadmin':
        superadmin_branch(message)
    else:
        bot.send_message(chat_id, 'Напишите /start');

# user branch***********************************************************
def user_branch(message):
    chat_id = message.chat.id
    global users
    try:
        users = openfile("users.db", chat_id)
    except:
        bot.send_message(chat_id, 'IO exception')
    else:
        print("db opened successfull")
    #     # for i, usr in enumerate(data['appealNum'], 0):
    #         # msg = (str(i) + usr['name'] + " has mail " + usr['mail'])
    #         # bot.send_message(chat_id, msg)
    bot.send_message(chat_id, welcome)
    generate_menu(themes, chat_id)
    # bot.register_next_step_handler(message, save_name)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global user
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    selTheme = 0
    for theme in themes:
        if call.data == theme[:3]: 
            # print(selTheme)
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f'Тема выбрана - {theme}')
            user.update({'selected_theme' : theme})
            bot.send_message(chat_id, f'debug stage: callback_worker: {user}')
    user_data(message)


def user_data(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Укажите своё ФИО')
    bot.register_next_step_handler(message, save_name)
    
def save_name(message):
    global user
    chat_id = message.chat.id
    name = message.text
    user.update({'user_id' : chat_id, 'name' : name})
    bot.send_message(chat_id, f'debug stage: save_name: {user}')
    bot.send_message(chat_id, f'Отлично, {name}. Теперь укажите свою почту')
    bot.register_next_step_handler(message, save_email)

def save_email(message):
    global user
    chat_id = message.chat.id
    email = message.text
    name = user['name']
    user.update({'email' : email})
    bot.send_message(chat_id, f'debug stage: save_email: {user}')
    bot.send_message(chat_id, f'Отлично, {name}. Ваша почта {email}. Теперь укажите свой телефон в формате +79001234567')
    bot.register_next_step_handler(message, save_phone)
    
def save_phone(message):
    chat_id = message.chat.id
    phone = message.text
    name = user['name']
    if phone[1:].isdigit():
        try: 
            carrier._is_mobile(number_type(phonenumbers.parse(phone)))
        except:
            bot.send_message(chat_id, f'Внимание, {name}, {phone} неверный!!')
            bot.register_next_step_handler(message, save_phone)
        else:
            bot.send_message(chat_id, f'Отлично, {name}. {phone} верный!\nТеперь укажите текст обращения.')
            user.update({'phone' : phone})
            bot.send_message(chat_id, f'debug stage: save_phone: {user}')
            # bot.register_next_step_handler(message, save_appeal)
    else:
        bot.send_message(chat_id, f'Внимание, {name}, {phone} - указан неверно, укажите заново!')
        bot.register_next_step_handler(message, save_phone)

# admin branch***********************************************************
def admin_branch(message):
    chat_id = message.chat.id
    generate_menu(admin_btn, chat_id)

# superadmin branch***********************************************************
def superadmin_branch(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "dummy superadmin_branch")



def openfile(name, chat_id):
    if(os.path.isfile(name)):
        with open(name, "r") as f:
            try:
                data = json.load(f)
            except:
                bot.send_message(chat_id, 'Something wrong with file!')
                print("foo")
                raise SystemExit("foobar", 0)
            else:
                # bot.send_message(chat_id, f'\ndata: {data}\n');
                return data
    else:             
        raise SystemExit(0)

def generate_menu(buttons, chat_id):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for element in buttons:
        # bot.send_message(chat_id, button)
        button = telebot.types.InlineKeyboardButton(text=element, callback_data=element[:3])
        keyboard.add(button)
    bot.send_message(chat_id, 'Выберите тему для обращения', reply_markup=keyboard)





            
bot.polling(non_stop=True, interval=1)

