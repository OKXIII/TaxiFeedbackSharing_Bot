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

_rus_chars = "УКЕНХВАРОСМТ"
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

#конвертация номеров в единый формат
def convert_licenseplate(lp):
    lp=lp.replace(" ","")
    trans=u''.join([_trans_table.get(c,c) for c in lp.upper()])
    return trans

#проверка номера на длину
def check_licenseplate_len(lp):
    result=True
    if len(lp)>10 or len(lp)<9: result=False
    return result

# проверка номера на символы
def check_licenseplate_chars(lp):
    result=True
    for i in lp:
        if i not in _permitted_chars:
            result=False
    return result

#получение информации из базы по номеру
def get_info_lp(lp):
    result=''
    db_worker = DB()
    result=db_worker.get_info_lp(lp)
    return result

#запись данных в БД
def save_new_lp(lp, comment):
    return




@bot.message_handler(commands=['start'])
def handle_start(message):
    msg = bot.send_message(message.chat.id, "Здравствуйте! Я телебот для обмена отзывами о таксистах.")
    # TODO: Добавить статистику о количестве пользователей сервиса и количестве отзывов
    request_lp(message)
    # Запись в лог
    pass


def request_lp(message):
    config._REQUEST_STEP = 0
    config._REQUEST_TYPE = 0
    bot.send_message(message.chat.id, "Укажите номер автомобиля")
    pass

# Статистика использования бота
@bot.message_handler(commands=['statistics'])
def handle_statistics(message):
    if message.chat.id == config.owner_chat_id:
        db_worker = DB()
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


#Формирование клавиатуры
def create_keyboard(type="common"):
    if type=="common":
        keyboard= types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        button_yes = types.KeyboardButton(text="Да")
        button_no = types.KeyboardButton(text="Нет")
        keyboard.add(button_yes, button_no)
    if type=="cancel":
        keyboard= types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        button_cancel = types.KeyboardButton(text="Отмена")
        keyboard.add(button_cancel)
    if type=="skip":
        keyboard= types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        button_skip = types.KeyboardButton(text="Пропустить")
        keyboard.add(button_skip)
    if type=="null":
        keyboard= types.ReplyKeyboardRemove()
    return keyboard


#Добавление нового номера
def add_new_lp(message):
    if config._REQUEST_TYPE == 1:
        config._REQUEST_TYPE=2
        config._REQUEST_STEP = 1
        bot.send_message(message.chat.id, "Введите ваш отзыв о такси с номером {0}".format(config.LICENSEPLATE),reply_markup=create_keyboard("cancel"))
        pass
    return

@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text==("Да") and (config._REQUEST_TYPE==1 or config._REQUEST_TYPE==2):
        add_new_lp(message)
        config._REQUEST_STEP = 1
        config._REQUEST_TYPE = 2
        #return
    if message.text==("Нет")  and (config._REQUEST_TYPE==1 or config._REQUEST_TYPE==2):

        request_lp(message)
        return
    if message.text==("Отмена")  and (config._REQUEST_TYPE==2):
        config._REQUEST_TYPE=0
        request_lp(message)
        return
    if message.text==("Пропустить")  and (config._REQUEST_TYPE==2):
        config._REQUEST_STEP+=1
        return

    if (config._REQUEST_TYPE==0):
        m=convert_licenseplate(message.text).upper()
        if not check_licenseplate_len(m):
            bot.send_message(message.chat.id, "Недопустимая длина номера автомобиля. Пожалуйста укажите правильный номер.")
            return
        if not check_licenseplate_chars(m):
            bot.send_message(message.chat.id, "В номере указаны неверные символы. Пожалуйста укажите правильный номер.")
            return
        config.LICENSEPLATE=m
        result_list=get_info_lp(m)
        if len(result_list)<1:
            config._REQUEST_TYPE=2
            bot.send_message(message.chat.id, "Информации по данному номеру нет. Хотите добавить?",reply_markup=create_keyboard())
        else:
            bot.send_message(message.chat.id, "Отзывы по номеру {0}".format(m))
            for item in result_list:
                text = "Дата: {0}".format(item[0])
                if item[1]!=None: text+="\nАвтомобиль: {0}".format(item[1])
                if item[2] != None: text+="\nКомментарий: {0}".format(item[2])
                if item[3] != None: text+="\nВодитель: {0}".format(item[3])
                if item[4] != None: text+="\nОценка: {0}".format(item[4])
                bot.send_message(message.chat.id, text)
            config._REQUEST_TYPE=2
            bot.send_message(message.chat.id, "Хотите добавить свой отзыв?",reply_markup=create_keyboard())

    if (config._REQUEST_TYPE==2):
        if config._REQUEST_STEP==1:
            config._REQUEST_STEP=2
            bot.send_message(message.chat.id, "Марка и модель автомобиля", reply_markup=create_keyboard("skip"))
            return
        if config._REQUEST_STEP==2:
            FDC['carmodel']=message.text
            config._REQUEST_STEP=3
            bot.send_message(message.chat.id, "Ваш комментарий о работе")
            return
        if config._REQUEST_STEP==3:
            FDC['comment']=message.text
            config._REQUEST_STEP=4
            bot.send_message(message.chat.id, "Как зовут водителя", reply_markup=create_keyboard("skip"))
            return
        if config._REQUEST_STEP==4:
            FDC['driver']=message.text
            config._REQUEST_STEP=5
            bot.send_message(message.chat.id, "Ваша оценка (1-5)", reply_markup=create_keyboard("skip"))
            return
        if config._REQUEST_STEP==5:
            FDC['grade']=message.text
            db_worker = DB()
            db_worker.save_comment(message.chat.id,config.LICENSEPLATE,FDC['carmodel'],FDC['comment'],FDC['driver'],FDC['grade'])
            db_worker.close()
            config._REQUEST_STEP = 0
            config._REQUEST_TYPE =0
            return

#TODO: проверка сообщения на длину
#TODO: проверка сообщения на корректность
#TODO: запись отзыва
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