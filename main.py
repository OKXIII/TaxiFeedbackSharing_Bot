# -*- coding: cp1251 -*-
#Версия 0.0.1

import config
import telebot
from telebot import types
#from database import DB
import random
import re
#import json
import time
import traceback

#_rus_chars = "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ"
_rus_chars = "УКЕНХВАРОСМТ"
_eng_chars = "YKEHXBAPOCMT"
_permitted_chars="QWERTYUIOPASDFGHJKLZXCVBNM1234567890"
_trans_table = dict(zip(_rus_chars, _eng_chars))

bot = telebot.TeleBot(config.token)

#конвертация номеров в единый формат
def convert_licenseplate(lp):
    trans=u''.join([_trans_table.get(c,c) for c in lp.upper()])
    res=''
    for i in trans:
        if i in _permitted_chars: res+=i
    return res  

#проверка номера на правильность

#получение информации из базы по номеру

#запись данных в БД




@bot.message_handler(commands=['start'])
def handle_start(message):
    msg = bot.send_message(message.chat.id, "Здравствуйте! Я телебот для обмена отзывами о таксистах. Укажите номер автомобиля")
    # Запись в лог
    pass


@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, convert_licenseplate(message.text).upper())
    pass


def telegram_polling():
    try:
        bot.polling(none_stop=True, timeout=123) #constantly get messages from Telegram
    except:
        traceback_error_string=traceback.format_exc()
        #with open("Error.Log", "a") as myfile:
        #    myfile.write("\r\n\r\n" + time.strftime("%c")+"\r\n<<error polling="">>\r\n"+ traceback_error_string + "\r\n<<error polling="">>")
        bot.stop_polling()
        time.sleep(10)
        #warning_to_owner("time: {0} \n error:\n {1} ".format(time.strftime("%c"),traceback_error_string) )
        telegram_polling()

if __name__ == '__main__':
    telegram_polling()