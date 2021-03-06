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
            self.cursor.execute("SELECT comment.time, comment.carmodel, comment.comment, comment.driver, comment.grade FROM licenseplate JOIN comment ON licenseplate.id=comment.license_plate_id WHERE licenseplate.licenseplate='{}'".format(src))
            result = self.cursor.fetchall()
        return result

    #Добавление записи в БД
    def save_comment(self, user_id, lp, carmodel, comment, driver, grade):
        with self.connection:
            self.cursor.execute("SELECT id from licenseplate WHERE licenseplate='{0}'".format(lp))
            licenseplate=self.cursor.fetchall()
            if len(licenseplate)==0:
                self.cursor.execute("INSERT INTO licenseplate (licenseplate,time) VALUES ('{0}','{1}')".format(lp,datetime.datetime.now()))
                self.cursor.execute("SELECT id from licenseplate WHERE licenseplate='{0}'".format(lp))
                licenseplate=self.cursor.fetchall()
            self.cursor.execute("INSERT INTO comment (grade, comment,driver,carmodel,license_plate_id, user_id, time) \
            VALUES ({0},'{1}','{2}','{3}',{4},'{5}','{6}')".format(grade,comment,driver,carmodel,licenseplate[0][0],user_id,datetime.datetime.now()))



#Получение статистики
    def get_count_licenseplate(self):
        with self.connection:
            self.cursor.execute("SELECT COUNT(DISTINCT licenseplate) FROM licenseplate")
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
            self.cursor.execute("SELECT COUNT(DISTINCT user_id) FROM comment")
            return self.cursor.fetchall()[0][0]

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()