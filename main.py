# -*- coding: cp1251 -*-
#Версия 0.0.1

import config
import telebot
from telebot import types
from database import DB
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
    lp=lp.replace(" ","")
    trans=u''.join([_trans_table.get(c,c) for c in lp.upper()])
    res=''
    for i in trans:
        if i in _permitted_chars:
            res+=i
        else:
            res+='O'
    return res

#проверка номера на правильность
def check_licenseplate(lp):
    result=True
    if len(lp)>10 or len(lp)<9: result=False
    return result

#получение информации из базы по номеру

#запись данных в БД




@bot.message_handler(commands=['start'])
def handle_start(message):
    msg = bot.send_message(message.chat.id, "Здравствуйте! Я телебот для обмена отзывами о таксистах. Укажите номер автомобиля")
    # Запись в лог
    pass

# Статистика использования бота
@bot.message_handler(commands=['statistics'])
def handle_statistics(message):
    if message.chat.id == config.owner_chat_id:
        db_worker = DB(config.database_name)
        count_licenseplates=db_worker.get_count_licenseplate()
        count_comments=db_worker.get_count_comment()
        count_photos=db_worker.get_count_photo()
        count_activeusers=db_worker.get_count_activeuser()
        text = "Активных пользователей - {0}\n" \
                "Автомобилей - {1}\n" \
                 "Комментариев - {2}\n" \
                 "Фотографий - {3}\n" \
             .format(count_activeusers,count_licenseplates,count_comments,count_photos)
        bot.send_message(message.chat.id, text)
        db_worker.close()
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