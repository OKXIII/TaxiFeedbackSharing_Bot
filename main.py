# -*- coding: cp1251 -*-
#������ 0.0.1

import config
import telebot
from telebot import types
#from database import DB
import random
import re
#import json
import time
import traceback

_rus_chars = "������������"
_eng_chars = "YKEHXBAPOCMT"
_trans_table = dict(zip(_rus_chars, _eng_chars))

bot = telebot.TeleBot(config.token)

#����������� ������� � ������ ������
def convert_licenseplate(lp):
    return u''.join([_trans_table.get(c,c) for c in lp])
    pass



#�������� ������ �� ������������

#��������� ���������� �� ���� �� ������

#������ ������ � ��




@bot.message_handler(commands=['start'])
def handle_start(message):
    msg = bot.send_message(message.chat.id, "������������! � ������� ��� ������ �������� � ���������. ������� ����� ����������")
    # ������ � ���
    pass


@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, convert_licenseplate(message.text))
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