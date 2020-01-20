# -*- coding: utf-8 -*-
# Версия 0.0.1

import config
import os
from urllib import parse
import psycopg2
import datetime

parse.uses_netloc.append("postgres")
try:
#    url = parse.urlparse(os.environ["DATABASE_URL"])
   url = parse.urlparse(os.environ["DATABASE_URL"])
except:
    print("*** DATABASE_URL not found", flush=True)


class DB:
    def __init__(self):
        # self.connection = sqlite3.connect(database)
        # self.cursor = self.connection.cursor()
        if config.mode == "test":
            self.connection = psycopg2.connect(
                dbname="database",
                user="postgres",
                password="123",
                host="localhost"
            )
        else:
            self.connection = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port)
        self.cursor = self.connection.cursor()

#Получение информации из БД
    def get_info_lp(self, src):
        with self.connection:
            self.cursor.execute("SELECT * FROM licenseplate WHERE licenseplate='{}'".format(src))
        return self.cursor.fetchall()[0]

    #Добавление записи в БД



#Получение статистики
    def get_count_licenseplate(self):
        with self.connection:
            self.cursor.execute("SELECT COUNT(id) FROM licenseplate")
            return self.cursor.fetchall()[0][0]

    def get_count_comment(self):
        with self.connection:
            self.cursor.execute("SELECT COUNT(id) FROM comment")
            return self.cursor.fetchall()[0][0]

    def get_count_photo(self):
        with self.connection:
            self.cursor.execute("SELECT COUNT(id) FROM photo")
            return self.cursor.fetchall()[0][0]

    def get_count_activeuser(self):
        with self.connection:
            self.cursor.execute("SELECT COUNT(user_id) FROM comment")
            return self.cursor.fetchall()[0][0]

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()