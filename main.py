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

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def handle_start(message):
    msg = bot.send_message(message.chat.id, "Здравствуйте! Я телебот для обмена отзывами о таксистах. Укажите номер автомобиля")
    # Запись в лог
    pass


#конвертация номеров в единый формат

