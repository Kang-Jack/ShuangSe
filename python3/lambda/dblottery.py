# virtulenv  easy_install MySQL-python  python2 pip install pymysql   Python 3. Use mysql-client or mysql-connect.
# pip install pymysql #mac
# import MySQLdb #for pc
import os
import sys

import pymysql as MySQL  # for mac
debug =0
db_host = os.environ['dbhost']  # URL of the site to check, stored in the site environment variable
db_user = os.environ['user']  # String expected to be on the page, stored in the expected environment variable
db_password = os.environ['pd']
db_db = os.environ['db']

class dblottery:
    host = db_host 
    user = db_user
    password = db_password
    db = db_db

    def __init__(self):
        self.connection = MySQL.connect(self.host, self.user, self.password, self.db, local_infile=1)
        self.cursor = self.connection.cursor()

    def operation_sql(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print("operation faild, Error:", e)

    def query(self, query):
        cursor = self.connection.cursor(MySQL.cursors.DictCursor)
        cursor.execute(query)
        return cursor.fetchall()

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    # =======================API for lotterydb=========================


    def insert_doubleball(self, identifier, lottery_date, r1, r2, r3, r4, r5, r6, b1):
        insert_sql = """
            INSERT INTO doubleball 
            (IDENTIFIER,GENERATE_TIME,RED1,RED2,RED3,RED4,RED5,RED6,BLUE) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
        try:
            if debug: print(insert_sql)
            self.cursor.execute(insert_sql, [identifier, lottery_date, r1, r2, r3, r4, r5, r6, b1])
            self.connection.commit()
            return insert_sql
        except MySQL.IntegrityError:
            pass
            print("duplicate indentifier %s" % identifier)
            return '0'
        except Exception as e:
            self.connection.rollback()
            print("operation faild, Error:", e)
            return '0'
