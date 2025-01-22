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
    global appealNum
    chat_id = message.chat.id
    if message.text == '/start':
        try:
            data = openfile("users.db", chat_id)
        except:
            bot.send_message(chat_id, 'IO exception');
        else:
            # for i, usr in enumerate(data['appealNum'], 0):
                # msg = (str(i) + usr['name'] + " has mail " + usr['mail'])
                # bot.send_message(chat_id, msg)
            bot.send_message(chat_id, welcome)
            generate_menu(themes, chat_id)
    elif message.text == '/admin':
        generate_menu(admin_btn, chat_id)
    else:
        bot.send_message(chat_id, 'Напишите /start');

    # appealNum += 1
    # # print(f'current appealNum: {appealNum}')
    # chat_id = message.chat.id
    # global userMode
    # keyboard = telebot.types.InlineKeyboardMarkup()
    # if message.text == '/start':
    #     bot.send_message(chat_id, "Добро пожаловать в бот пользователь:");
    #     userMode = 1
    #     # testFun(message)
    #     # return True
    #     for i in range(len(themes)):
    #         button[i] = telebot.types.InlineKeyboardButton(text=themes[i], callback_data=f'{i}')
    #         keyboard.row(button[i])
    #     bot.send_message(chat_id, 'Выберите тему для обращения', reply_markup=keyboard)
    # elif message.text == '/admin':
    #     # testFun(message)
    #     # return True
    #     for i in range(len(admin_btn)):
    #         button[i] = telebot.types.InlineKeyboardButton(text=admin_btn[i], callback_data=admin_btn_callback[i])
    #         keyboard.add(button[i])
    #     bot.send_message(chat_id, 'Административная панель:', reply_markup=keyboard)
    # else:
    #     bot.send_message(chat_id, 'Напишите /start');

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

