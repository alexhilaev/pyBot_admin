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