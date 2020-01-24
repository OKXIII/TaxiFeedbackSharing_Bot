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

FDC={
    'licenseplate':'',
    'carmodel':'',
    'driver':'',
    'comment':'',
    'grade': 0
}


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
def save_new_lp(lp, comment):
    return




@bot.message_handler(commands=['start'])
def handle_start(message):
    msg = bot.send_message(message.chat.id, "������������! � ������� ��� ������ �������� � ���������.")
    # TODO: �������� ���������� � ���������� ������������� ������� � ���������� �������
    request_lp(message)
    # ������ � ���
    pass


def request_lp(message):
    config._REQUEST_STEP = 0
    config._REQUEST_TYPE = 0
    bot.send_message(message.chat.id, "������� ����� ����������")
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
    if type=="common":
        keyboard= types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        button_yes = types.KeyboardButton(text="��")
        button_no = types.KeyboardButton(text="���")
        keyboard.add(button_yes, button_no)
    if type=="cancel":
        keyboard= types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        button_cancel = types.KeyboardButton(text="������")
        keyboard.add(button_cancel)
    if type=="skip":
        keyboard= types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        button_skip = types.KeyboardButton(text="����������")
        keyboard.add(button_skip)
    if type=="null":
        keyboard= types.ReplyKeyboardRemove()
    return keyboard


#���������� ������ ������
def add_new_lp(message):
    if config._REQUEST_TYPE == 1:
        config._REQUEST_TYPE=2
        config._REQUEST_STEP = 1
        bot.send_message(message.chat.id, "������� ��� ����� � ����� � ������� {0}".format(config.LICENSEPLATE),reply_markup=create_keyboard("cancel"))
        pass
    return

@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text==("��") and (config._REQUEST_TYPE==1 or config._REQUEST_TYPE==2):
        add_new_lp(message)
        config._REQUEST_STEP = 1
        config._REQUEST_TYPE = 2
        #return
    if message.text==("���")  and (config._REQUEST_TYPE==1 or config._REQUEST_TYPE==2):

        request_lp(message)
        return
    if message.text==("������")  and (config._REQUEST_TYPE==2):
        config._REQUEST_TYPE=0
        request_lp(message)
        return
    if message.text==("����������")  and (config._REQUEST_TYPE==2):
        config._REQUEST_STEP+=1
        return

    if (config._REQUEST_TYPE==0):
        m=convert_licenseplate(message.text).upper()
        if not check_licenseplate_len(m):
            bot.send_message(message.chat.id, "������������ ����� ������ ����������. ���������� ������� ���������� �����.")
            return
        if not check_licenseplate_chars(m):
            bot.send_message(message.chat.id, "� ������ ������� �������� �������. ���������� ������� ���������� �����.")
            return
        config.LICENSEPLATE=m
        result_list=get_info_lp(m)
        if len(result_list)<1:
            config._REQUEST_TYPE=2
            bot.send_message(message.chat.id, "���������� �� ������� ������ ���. ������ ��������?",reply_markup=create_keyboard())
        else:
            bot.send_message(message.chat.id, "������ �� ������ {0}".format(m))
            for item in result_list:
                text = "����: {0}".format(item[0])
                if item[1]!=None: text+="\n����������: {0}".format(item[1])
                if item[2] != None: text+="\n�����������: {0}".format(item[2])
                if item[3] != None: text+="\n��������: {0}".format(item[3])
                if item[4] != None: text+="\n������: {0}".format(item[4])
                bot.send_message(message.chat.id, text)
            config._REQUEST_TYPE=2
            bot.send_message(message.chat.id, "������ �������� ���� �����?",reply_markup=create_keyboard())

    if (config._REQUEST_TYPE==2):
        if config._REQUEST_STEP==1:
            config._REQUEST_STEP=2
            bot.send_message(message.chat.id, "����� � ������ ����������", reply_markup=create_keyboard("skip"))
            return
        if config._REQUEST_STEP==2:
            FDC['carmodel']=message.text
            config._REQUEST_STEP=3
            bot.send_message(message.chat.id, "��� ����������� � ������")
            return
        if config._REQUEST_STEP==3:
            FDC['comment']=message.text
            config._REQUEST_STEP=4
            bot.send_message(message.chat.id, "��� ����� ��������", reply_markup=create_keyboard("skip"))
            return
        if config._REQUEST_STEP==4:
            FDC['driver']=message.text
            config._REQUEST_STEP=5
            bot.send_message(message.chat.id, "���� ������ (1-5)", reply_markup=create_keyboard("skip"))
            return
        if config._REQUEST_STEP==5:
            FDC['grade']=message.text
            db_worker = DB()
            db_worker.save_comment(message.chat.id,config.LICENSEPLATE,FDC['carmodel'],FDC['comment'],FDC['driver'],FDC['grade'])
            db_worker.close()
            config._REQUEST_STEP = 0
            config._REQUEST_TYPE =0
            return

#TODO: �������� ��������� �� �����
#TODO: �������� ��������� �� ������������
#TODO: ������ ������
        return

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