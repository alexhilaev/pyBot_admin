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

users = {}
admins = {}
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

def testFun(message):
    global appealNum
    chat_id = message.chat.id
    users['appealNum'] = appealNum
    users['prop'] = {}
    users['prop']['chat_id'] = chat_id
    users['prop']['name'] = "qwe"
    users['prop']['email'] = "qwe"
    users['prop']['phone'] = "+789"
    users['prop']['appeal'] = "qwe qwe"
    users['prop']['status'] = "opened"
    finish(message)


@bot.message_handler(content_types=['text'])
def start(message):
    global appealNum
    if(os.path.isfile("data.json")):
        with open("data.json", "r") as f:
            try:
                data = json.load(f)
                # print(f'\ndata: {data}\n')
            except:
                print('Something wrong with file!')
            else:
                try:
                    appealNums = list(map(lambda x: x['appealNum'], data))
                    # print(f'appealNums: {appealNums}')
                except:
                    print("No appealNum\n")
                else:
                    appealNum = appealNums[-1]
                    # print(f'last appealNum: {appealNums[-1]}')

    appealNum += 1
    # print(f'current appealNum: {appealNum}')
    chat_id = message.chat.id
    global userMode
    keyboard = telebot.types.InlineKeyboardMarkup()
    if message.text == '/start':
        bot.send_message(chat_id, "Добро пожаловать в бот пользователь:");
        userMode = 1
        # testFun(message)
        # return True
        for i in range(len(themes)):
            button[i] = telebot.types.InlineKeyboardButton(text=themes[i], callback_data=f'{i}')
            keyboard.row(button[i])
        bot.send_message(chat_id, 'Выберите тему для обращения', reply_markup=keyboard)
    elif message.text == '/admin':
        # testFun(message)
        # return True
        for i in range(len(admin_btn)):
            button[i] = telebot.types.InlineKeyboardButton(text=admin_btn[i], callback_data=admin_btn_callback[i])
            keyboard.add(button[i])
        bot.send_message(chat_id, 'Административная панель:', reply_markup=keyboard)
    else:
        bot.send_message(chat_id, 'Напишите /start');

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    selTheme = 0
    keyboard = telebot.types.InlineKeyboardMarkup()
    global themeReg
    if userMode == 1:
        users['prop'] = {}
        for i in range(len(themes)):
            if call.data == f'{i}': 
                selTheme = i
                # print(selTheme)
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f'Тема выбрана - {themes[selTheme]}')
                users['prop']['selected_theme'] = themes[selTheme]
        user_data(message)
    elif userMode == 0 and themeReg == 0:
        if call.data == "appeal_all_view":
            bot.send_message(chat_id, "Просмотр открытых обращений")
            view_opened_appeals(message)
            # bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f'menu kill')
        if call.data == "register":
            # bot.send_message(chat_id, "Выберите тему для добавления")
            for i in range(len(themes)):
                # bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f'menu kill1')
                button[i] = telebot.types.InlineKeyboardButton(text=themes[i], callback_data=f'{i}')
                keyboard.add(button[i])
            themeReg = 1
            bot.send_message(chat_id, 'Добавьте тему для получения рассылки:', reply_markup=keyboard)
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f'menu kill')
        start(message)
    elif userMode == 0 and themeReg == 1:
        # print("test")
        # print(call.data)
        for i in range(len(themes)):
            print(f'{i}')
            if call.data == f'{i}': 
                selTheme = i
                print(selTheme)
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f'Тема выбрана - {themes[selTheme]}')
                # admins['prop'][adminThemesList] = themes[selTheme]
                # print(admins, themes[selTheme])
        theme_reg(message, themes[selTheme])


def user_data(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Укажите своё ФИО')
    users['appealNum'] = appealNum
    users['prop']['chat_id'] = chat_id
    bot.register_next_step_handler(message, save_name)
    
def save_name(message):
    chat_id = message.chat.id
    name = message.text
    users['prop']['name'] = name
    bot.send_message(chat_id, f'Отлично, {name} {chat_id}. Теперь укажите свою почту')
    bot.register_next_step_handler(message, save_email)

def save_email(message):
    chat_id = message.chat.id
    email = message.text
    name = users['prop']['name']
    users['prop']['email'] = email
    bot.send_message(chat_id, f'Отлично, {name} {chat_id}. Ваша почта {email}. Теперь укажите свой телефон в формате +79001234567')
    bot.register_next_step_handler(message, save_phone)
    
def save_phone(message):
    chat_id = message.chat.id
    phone = message.text
    name = users['prop']['name']
    users['prop']['phone'] = phone
    if phone[1:].isdigit():
        try: 
            carrier._is_mobile(number_type(phonenumbers.parse(phone)))
        except:
            bot.send_message(chat_id, f'Внимание, {name} {chat_id}, {phone} неверный!!')
            bot.register_next_step_handler(message, save_phone)
        else:
            bot.send_message(chat_id, f'Отлично, {name} {chat_id}. {phone} верный!\nТеперь укажите текст обращения.')
            bot.register_next_step_handler(message, save_appeal)
    else:
        bot.send_message(chat_id, f'Внимание, {name} {chat_id}, {phone} - указан неверно, укажите заново!')
        bot.register_next_step_handler(message, save_phone)

def save_appeal(message):
    global appealNum
    chat_id = message.chat.id
    appeal = message.text
    name = users['prop']['name']
    email = users['prop']['email']
    phone = users['prop']['phone']
    selected_theme = users['prop']['selected_theme']
    users['prop']['appeal'] = appeal
    users['prop']['status'] = "opened"
    bot.send_message(chat_id, f'Отлично, {name} {chat_id}.\n'
        f'Ваша почта {email}, телефон {phone}\n'
        f'Текст обращения:\n\"{appeal}\"\n'
        f'Выбранная тема: {selected_theme}\n'
        f'Номер заявки: {appealNum}')
    finish(message)

def view_opened_appeals(message):
    chat_id = message.chat.id
    if(os.path.isfile("data.json")):
        with open("data.json", "r") as f:
            try:
                userList = json.load(f)
            except:
                bot.send_message(chat_id, 'Something wrong with file!')
                # print('Something wrong with file!')
            else:
                # bot.send_message(chat_id, f'loaded userList: {userList}')
                # print(len(userList))
                for x in userList:
                    try:
                        bot.send_message(chat_id, ("Номер обращения: " + str(x['appealNum']) +\
                        "\nФИО: " + x['prop']['name'] +\
                        "\nEmail: " + x['prop']['email'] +\
                        "\nТелефон: " + x['prop']['phone'] +\
                        "\nСтатус: " + x['prop']['status'] +\
                        "\nТекст обращения: " + x['prop']['appeal']))
                    except:
                        bot.send_message(chat_id, "Поврежденная строка: " + str(x))
                    # bot.send_message(chat_id, ("****************************************"))
    message.text = '/admin'
    start(message)

# register theme for admin
def theme_reg(message, selTheme):
    global admins
    global adminThemesList
    global userMode
    global adminList
    global themeReg
    chat_id = message.chat.id
    # print(admins)
    admins[chat_id] = {}
    admins[chat_id]['adminThemesList'] = []
    admins[chat_id]['name'] = bot.get_chat_member(chat_id, chat_id).user.username
    bot.send_message(chat_id, "test theme: " + selTheme)
    themeReg = 0
    chat_id = message.chat.id
    if(os.path.isfile("data_admins.json")):
        with open("data_admins.json", "r") as f:
            try:
                adminList = json.load(f)
            except:
                print('Something wrong with file!')
            else:
                print(f'loaded userList: {adminList}')
    if(adminList[chat_id] == chat_id and (selTheme not in adminList[chat_id]['adminThemesList'])):
        admins[chat_id]['adminThemesList'].append(selTheme)
    adminList.update(admins)
    # data.update(users)
    # print(f'\ndata: {data}\n')
    bot.send_message(chat_id, f'\nadmins: {admins}\n')
    bot.send_message(chat_id, f'\nadminList: {adminList}\n')
    with open('data_admins.json', 'w') as f:
        json.dump(adminList, f)
    name = admins[chat_id]['name']
    bot.send_message(chat_id, f'{name} chatid={chat_id}, зарегана тема {selTheme}')



def finish(message):
    global userList
    global userMode
    chat_id = message.chat.id
    if(os.path.isfile("data.json")):
        with open("data.json", "r") as f:
            try:
                userList = json.load(f)
            except:
                print('Something wrong with file!')
            else:
                print(f'loaded userList: {userList}')
    userList.append(users)
    # data.update(users)
    # print(f'\ndata: {data}\n')
    print(f'\nusers: {users}\n')
    print(f'\nuserList: {userList}\n')
    with open('data.json', 'w') as f:
        json.dump(userList, f)
    name = users['prop']['name']
    bot.send_message(chat_id, f'{name} chatid={chat_id}, ожидайте ответа в течение 7 дней.')
    # bot.forward_message(chat_id='@nrzx3', from_chat_id=chat_id, message_id=message.id)
    # bot.register_next_step_handler(message, save_surname)
    # start(message)
    userMode = 0

bot.polling(non_stop=True, interval=1)
