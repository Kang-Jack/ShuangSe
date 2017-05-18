import dblottery
from pandas import DataFrame, Series
import pandas as pd
import numpy as np
debug=1
db = dblottery.dblottery()

def get_one_year_data_(year):
    data=[]
    rows =db.query(r"SELECT * FROM lottery.doubleball where doubleball.GENERATE_TIME like '"+year+"%'")
    for row in rows:
        data.append(parse_row_data(row))
        if debug==1: print str(rows[0]["IDENTIFIER"])
        if debug==1: print rows[0]["GENERATE_TIME"].strip("\"")
        if debug==1: print rows[0]["RED1"].strip("\"")
    #if debug==1: print data
    return data

def get_data_indentifier_range(year_begin,year_end):
    rows =db.query(r"SELECT * FROM lottery.doubleball where doubleball.IDENTIFIER between "+year_begin+" and "+ year_end )
    #for row in rows:
    if debug==1: print str(rows[0]["IDENTIFIER"])
    if debug==1: print rows[0]["GENERATE_TIME"].strip("\"")
    if debug==1: print rows[0]["RED1"].strip("\"")
    if debug==1: print str(rows[len(rows)-1]["IDENTIFIER"]).strip("\"")
    if debug==1: print rows[len(rows)-1]["GENERATE_TIME"].strip("\"")
    if debug==1: print rows[len(rows)-1]["RED1"].strip("\"")


def get_all_data():
    rows =db.query(r"SELECT * FROM lottery.doubleball where 1=1 " )
    #for row in rows:
    if debug==1: print str(rows[0]["IDENTIFIER"])
    if debug==1: print rows[0]["GENERATE_TIME"].strip("\"")
    if debug==1: print rows[0]["RED1"].strip("\"")
    if debug==1: print str(rows[len(rows)-1]["IDENTIFIER"]).strip("\"")
    if debug==1: print rows[len(rows)-1]["GENERATE_TIME"].strip("\"")
    if debug==1: print rows[len(rows)-1]["RED1"].strip("\"")

def parse_row_data(row):
    return [row["IDENTIFIER"],row["GENERATE_TIME"].strip("\""),row["RED1"].strip("\""),\
    row["RED2"].strip("\""),row["RED3"].strip("\""),row["RED4"].strip("\""),\
    row["RED5"].strip("\""),row["RED6"].strip("\""),row["BLUE"].strip("\"")]

if __name__ == '__main__':
    rs=get_one_year_data_('2008')
    #get_data_indentifier_range('2009001','2010160')
    frame =DataFrame(rs)
    print  frame[0][:10]
    frame[0][:10].plot(kind='barh',rot=0)
    print frame.values[0]