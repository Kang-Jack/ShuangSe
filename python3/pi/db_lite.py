# virtulenv  easy_install MySQL-python  python2 pip install pymysql   Python 3. Use mysql-client or mysql-connect.
#pip install pymysql #mac
#import MySQLdb #for pc
import csv
import sys

#import pymysql as MySQL #for mac
import sqlite3

import datetime

class dblotterylite:

    #host = 'localhost' #'8.34.215.127''localhost'
    #user = 'root'
    #password = 'd2000'
    db = 'lottery.db'

    def __init__(self):
        self.connection = sqlite3.connect(self.db)
        self.cursor = self.connection.cursor()

    def operation_sql(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except:
            e = sys.exc_info()[0]
            self.connection.rollback()
            print("operation faild, Error:", e)

    def query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def __del__(self):
        self .cursor.close()
        self.connection.close()

    #=======================API for lotterydb=========================


    def insert_doubleball(self,identifier, lottery_date, r1 ,r2, r3, r4, r5,r6,b1):
        insert_sql = """
            INSERT INTO doubleball 
            (IDENTIFIER,GENERATE_TIME,RED1,RED2,RED3,RED4,RED5,RED6,BLUE) 
            VALUES (?,?,?,?,?,?,?,?,?)
            """
        try:
            print (insert_sql)
            self.cursor.execute(insert_sql, (identifier, lottery_date, r1 ,r2, r3, r4, r5,r6,b1))
            self.connection.commit()
            return 1
        except sqlite3.Error as lite_e:
            pass
            print("duplicate indentifier %s" % (identifier))
            print("Error message %s" % (lite_e))
            return 0
        except:
            e = sys.exc_info()[0]
            self.connection.rollback()
            print("operation faild, Error:", e)
            return 0




