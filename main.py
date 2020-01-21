# -*- coding: cp1251 -*-
#������ 0.0.1

import config
import telebot
from telebot import types
from database import DB
import random
import re
#import json
import time
import traceback

_rus_chars = "������������"
_eng_chars = "YKEHXBAPOCMT"
_permitted_chars="QWERTYUIOPASDFGHJKLZXCVBNM1234567890"
_trans_table = dict(zip(_rus_chars, _eng_chars))

#��� �������
#0 - �� ���������
#1 - ������ �� �������� ������ ������
#2 - ������ �� ���������� �����������
_REQUEST_TYPE=0


bot = telebot.TeleBot(config.token)

#����������� ������� � ������ ������
def convert_licenseplate(lp):
    lp=lp.replace(" ","")
    trans=u''.join([_trans_table.get(c,c) for c in lp.upper()])
    return trans

#�������� ������ �� �����
def check_licenseplate_len(lp):
    result=True
    if len(lp)>10 or len(lp)<9: result=False
    return result

# �������� ������ �� �������
def check_licenseplate_chars(lp):
    result=True
    for i in lp:
        if i not in _permitted_chars:
            result=False
    return result

#��������� ���������� �� ���� �� ������
def get_info_lp(lp):
    result=''
    db_worker = DB()
    result=db_worker.get_info_lp(lp)
    return result

#������ ������ � ��




@bot.message_handler(commands=['start'])
def handle_start(message):
    msg = bot.send_message(message.chat.id, "������������! � ������� ��� ������ �������� � ���������. ������� ����� ����������")
    request_lp(message)
    # ������ � ���
    pass


def request_lp(message):
    msg = bot.send_message(message.chat.id, "������� ����� ����������")
    pass

# ���������� ������������� ����
@bot.message_handler(commands=['statistics'])
def handle_statistics(message):
    if message.chat.id == config.owner_chat_id:
        db_worker = DB()
        count_licenseplates=db_worker.get_count_licenseplate()
        count_comments=db_worker.get_count_comment()
        count_photos=db_worker.get_count_photo()
        count_activeusers=db_worker.get_count_activeuser()
        text = "�������� ������������� - {0}\n" \
                "����������� - {1}\n" \
                 "������������ - {2}\n" \
                 "���������� - {3}\n" \
             .format(count_activeusers,count_licenseplates,count_comments,count_photos)
        bot.send_message(message.chat.id, text)
        db_worker.close()
    pass


#������������ ����������
def create_keyboard(type="common"):
    keyboard= types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_yes = types.KeyboardButton(text="��")
    button_no = types.KeyboardButton(text="���")
    keyboard.add(button_yes, button_no)
    return keyboard

#���������� ������ ������
def add_new_lp(message):
    if _REQUEST_TYPE == 1:
        bot.send_message(message.chat.id, "��������� ����� �����")
        pass
    if _REQUEST_TYPE == 2:
        bot.send_message(message.chat.id, "��������� ����� �����������")
        pass
    return

@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text==("��"):
        add_new_lp(message)
        return
    if message.text==("���"):
        request_lp(message)
        return


    m=convert_licenseplate(message.text).upper()
    if not check_licenseplate_len(m):
        bot.send_message(message.chat.id, "������������ ����� ������ ����������. ���������� ������� ���������� �����.")
        return
    if not check_licenseplate_chars(m):
        bot.send_message(message.chat.id, "� ������ ������� �������� �������. ���������� ������� ���������� �����.")
        return
    r=get_info_lp(m)
    if len(r)<1:
        _REQUEST_TYPE=1
        bot.send_message(message.chat.id, "���������� �� ������� ������ ���. ������ ��������?",reply_markup=create_keyboard())
    else:
        bot.send_message(message.chat.id, r)
        _REQUEST_TYPE=2
        bot.send_message(message.chat.id, "������ �������� ���� �����?",reply_markup=create_keyboard())
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