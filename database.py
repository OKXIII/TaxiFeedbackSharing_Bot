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
   url = parse.urlparse(os.environ["DATABASE"])
except:
    print("*** DATABASE_URL not found", flush=True)


class DB:
    def __init__(self, database):
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


    def get_count_licenseplate(self):
        with self.connection:
            self.cursor.execute("SELECT COUNT(ID) FROM [License plate]")
            return self.cursor.fetchall()[0][0]

    def get_count_comment(self):
        with self.connection:
            self.cursor.execute("SELECT COUNT(ID) FROM [Comment]")
            return self.cursor.fetchall()[0][0]

    def get_count_photo(self):
        with self.connection:
            self.cursor.execute("SELECT COUNT(ID) FROM [Photo]")
            return self.cursor.fetchall()[0][0]

    def get_count_activeuser(self):
        with self.connection:
            self.cursor.execute("SELECT COUNT(User_id) FROM [Comment]")
            return self.cursor.fetchall()[0][0]