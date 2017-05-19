import dblottery
from pandas import DataFrame, Series
import pandas as pd
import numpy as np
import matrix
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
    data=[]
    rows =db.query(r"SELECT * FROM lottery.doubleball where doubleball.IDENTIFIER between "+year_begin+" and "+ year_end )
    for row in rows:
        data.append(parse_row_data(row))
    if debug==1: print str(rows[0]["IDENTIFIER"])
    if debug==1: print rows[0]["GENERATE_TIME"].strip("\"")
    if debug==1: print rows[0]["RED1"].strip("\"")
    if debug==1: print str(rows[len(rows)-1]["IDENTIFIER"]).strip("\"")
    if debug==1: print rows[len(rows)-1]["GENERATE_TIME"].strip("\"")
    if debug==1: print rows[len(rows)-1]["RED1"].strip("\"")
    #if debug==1: print data
    return data

def get_all_data():
    data=[]
    rows =db.query(r"SELECT * FROM lottery.doubleball where 1=1 " )
    for row in rows:
        data.append(parse_row_data(row))
    if debug==1: print str(rows[0]["IDENTIFIER"])
    if debug==1: print rows[0]["GENERATE_TIME"].strip("\"")
    if debug==1: print rows[0]["RED1"].strip("\"")
    if debug==1: print str(rows[len(rows)-1]["IDENTIFIER"]).strip("\"")
    if debug==1: print rows[len(rows)-1]["GENERATE_TIME"].strip("\"")
    if debug==1: print rows[len(rows)-1]["RED1"].strip("\"")
    return data

def calc_per(num,total):
    return "%.2f%%" % (float(num)/float(total)*100)

def parse_row_data(row):
    return [row["IDENTIFIER"],row["GENERATE_TIME"].strip("\""),row["RED1"].strip("\""),\
    row["RED2"].strip("\""),row["RED3"].strip("\""),row["RED4"].strip("\""),\
    row["RED5"].strip("\""),row["RED6"].strip("\""),row["BLUE"].strip("\"")]

def append_sum(df,isBlue):
    count = len(df.index)
    if count <1:
        return
    maxN = 34
    if isBlue :
        maxN=17
    append_data = [[0 for i in range(maxN)] for i in range (2)]
    #print append_data
    sumN=0
    for i in range (1,maxN):
        if debug==1:print i
        append_data[0][i] = sum(df[i])
        sumN=sumN+append_data[0][i]
        append_data[1][i] = calc_per(append_data[0][i],count)
    if debug==1:print sumN
    return append_data




if __name__ == '__main__':
    #rs=get_one_year_data_('2008')
    rs=get_all_data()
    if debug==1:print len(rs)
    if debug==1:print (rs[0])
    if debug==1:print (rs[153])
    #get_data_indentifier_range('2009001','2010160')
    red_matrix_frame = DataFrame(matrix.matrix_data.parse_red_balls(rs))
    #print red_matrix_frame.count()
    blue_matrix_frame = DataFrame(matrix.matrix_data.parse_blue_ball(rs))
    map_frame = DataFrame(matrix.matrix_data.parse_date_id_map(rs))
    if debug==1:print append_sum(red_matrix_frame,False)
    if debug==1:print append_sum(blue_matrix_frame,True)
    #print calc_per(sum(red_matrix_frame[1]),len(rs))
    #print red_matrix_frame
    #print blue_matrix_frame
    #print map_frame

    #frame =DataFrame(rs)
    #print  frame[0][:10]
    #frame[0][:10].plot(kind='barh',rot=0)
    #print frame.values[0]