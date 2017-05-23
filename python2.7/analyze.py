import dblottery
from pandas import DataFrame, Series
import pandas as pd
import numpy as np
import time
import sys, getopt
from census import census_data
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

def parse_row_data(row):
    return [row["IDENTIFIER"],row["GENERATE_TIME"].strip("\""),row["RED1"].strip("\""),\
    row["RED2"].strip("\""),row["RED3"].strip("\""),row["RED4"].strip("\""),\
    row["RED5"].strip("\""),row["RED6"].strip("\""),row["BLUE"].strip("\"")]

def usage():
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
    #rs = get_data_indentifier_range('2013001','2013160')
    #rs=get_all_data()
    if debug==1:print len(rs)
    if debug==1:print (rs[0])
    if debug==1:print (rs[len(rs)-1])

    red_matrix_frame = DataFrame(census_data.get_red_matrix(rs))
    blue_matrix_frame = DataFrame(census_data.get_blue_matrix(rs))
    map_frame = DataFrame(census_data.get_date_id_map(rs))
    red_matrix_frame = red_matrix_frame.append (census_data.get_sum_info(red_matrix_frame,False))
    #blue_matrix_frame = blue_matrix_frame.append (census_data.get_sum_info(blue_matrix_frame,True))
    ts= str(time.time())
    print ts
    #red_matrix_frame.to_csv(r"./result/redALL"+ts+".csv",index=False)
    #blue_matrix_frame.to_csv(r"./result/blueALL"+ts+".csv",index=False)
    #map_frame.to_csv(r"./result/mapALL"+ts+".csv",index=False)
    #if debug==1:print census_data.get_sum_info(red_matrix_frame,False)
    #if debug==1:print census_data.get_sum_info(blue_matrix_frame,True)
    #print calc_per(sum(red_matrix_frame[1]),len(rs))
    print red_matrix_frame.tail(3)
    print blue_matrix_frame.tail(3)
    census_data.find_same_rate_scale_blue(blue_matrix_frame)
    #print blue_matrix_frame
    #print map_frame

    #frame =DataFrame(rs)
    #print  frame[0][:10]
    #frame[0][:10].plot(kind='barh',rot=0)
    #print frame.values[0]