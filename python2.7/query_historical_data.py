import dblottery
from pandas import DataFrame, Series
import pandas as pd
import numpy as np
import time
import sys, getopt
debug=1

class historical_data:
    db = dblottery.dblottery()
    def __init__(self):
        self.db = dblottery.dblottery()

    def get_one_year_data_(self,year):
        data=[]
        rows =self.db.query(r"SELECT * FROM lottery.doubleball where doubleball.GENERATE_TIME like '"+year+"%'")
        for row in rows:
            data.append(self.parse_row_data(row))
        if debug==1: print str(rows[0]["IDENTIFIER"])
        if debug==1: print rows[0]["GENERATE_TIME"].strip("\"")
        if debug==1: print rows[0]["RED1"].strip("\"")
        #if debug==1: print data
        return data

    def get_data_indentifier_range(self,year_begin,year_end):
        data=[]
        rows =self.db.query(r"SELECT * FROM lottery.doubleball where doubleball.IDENTIFIER between "+year_begin+" and "+ year_end )
        for row in rows:
            data.append(self.parse_row_data(row))
        if debug==1: print str(rows[0]["IDENTIFIER"])
        if debug==1: print rows[0]["GENERATE_TIME"].strip("\"")
        if debug==1: print rows[0]["RED1"].strip("\"")
        if debug==1: print str(rows[len(rows)-1]["IDENTIFIER"]).strip("\"")
        if debug==1: print rows[len(rows)-1]["GENERATE_TIME"].strip("\"")
        if debug==1: print rows[len(rows)-1]["RED1"].strip("\"")
        #if debug==1: print data
        return data
        
    def get_all_data(self):
        data=[]
        rows =self.db.query(r"SELECT * FROM lottery.doubleball where 1=1 " )
        for row in rows:
            data.append(self.parse_row_data(row))
        if debug==1: print str(rows[0]["IDENTIFIER"])
        if debug==1: print rows[0]["GENERATE_TIME"].strip("\"")
        if debug==1: print rows[0]["RED1"].strip("\"")
        if debug==1: print str(rows[len(rows)-1]["IDENTIFIER"]).strip("\"")
        if debug==1: print rows[len(rows)-1]["GENERATE_TIME"].strip("\"")
        if debug==1: print rows[len(rows)-1]["RED1"].strip("\"")
        return data

    def parse_row_data(self,row):
        return [row["IDENTIFIER"],row["GENERATE_TIME"].strip("\""),row["RED1"].strip("\""),\
        row["RED2"].strip("\""),row["RED3"].strip("\""),row["RED4"].strip("\""),\
        row["RED5"].strip("\""),row["RED6"].strip("\""),row["BLUE"].strip("\"")]


    def usage(self):
        print (r'Get all data by default')
        print (r'-s: Start of lottery No.')
        print (r'-e: End of  lottery No.')
        print (r'-y: Get single year data')
        print (r'-h: Help')

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], 'hs:e:y:')
    startNo=''
    endNo=''
    singleY=''
    for op, value in opts:
        if op == '-s':
            startNo = value
        elif op == '-e':
            endNo = value
        elif op == '-y':
            singleY = value
        elif op == '-h':
            usage()
            sys.exit()
    if debug : print startNo
    if debug : print endNo
    if debug : print singleY
    rs=[]
    if startNo != '' and endNo !='':
        rs = get_data_indentifier_range(startNo,endNo)
    elif singleY !='':
        rs = get_one_year_data_(singleY)
    else:
        rs = get_all_data()