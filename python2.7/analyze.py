import dblottery
from pandas import DataFrame, Series
import pandas as pd
import numpy as np
import time
import sys, getopt
from census import census_data
from query_historical_data import historical_data
debug=1
db = dblottery.dblottery()
historical_data=historical_data()

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
            historical_data.usage()
            sys.exit()
    if debug : print startNo
    if debug : print endNo
    if debug : print singleY
    rs=[]
    if startNo != '' and endNo !='':
        rs = historical_data.get_data_indentifier_range(startNo,endNo)
    elif singleY !='':
        rs = historical_data.get_one_year_data(singleY)
    else:
        rs = historical_data.get_all_data()
    #rs = get_data_indentifier_range('2013001','2013160')
    #rs=get_all_data()
    if debug==1:print len(rs)
    if debug==1:print (rs[0])
    if debug==1:print (rs[len(rs)-1])

    red_matrix_frame = DataFrame(census_data.get_red_matrix(rs))
    blue_matrix_frame = DataFrame(census_data.get_blue_matrix(rs))
    map_frame = DataFrame(census_data.get_date_id_map(rs))

    ts= str(time.time())
    print ts
    #red_matrix_frame.to_csv(r"./result/redALL"+ts+".csv",index=False)
    #blue_matrix_frame.to_csv(r"./result/blueALL"+ts+".csv",index=False)
    #map_frame.to_csv(r"./result/mapALL"+ts+".csv",index=False)
    #if debug==1:print census_data.get_sum_info(red_matrix_frame,False)
    #if debug==1:print census_data.get_sum_info(blue_matrix_frame,True)
    #print calc_per(sum(red_matrix_frame[1]),len(rs))
    if debug==1:print red_matrix_frame.tail(3)
    if debug==1:print blue_matrix_frame.tail(3)
    census_data.find_same_rate_scale_blue(blue_matrix_frame)
    #print blue_matrix_frame
    #print map_frame

    #frame =DataFrame(rs)
    #print  frame[0][:10]
    #frame[0][:10].plot(kind='barh',rot=0)
    #print frame.values[0]
    #red_matrix_frame = red_matrix_frame.append (census_data.get_sum_info(red_matrix_frame,False))
    #blue_matrix_frame = blue_matrix_frame.append (census_data.get_sum_info(blue_matrix_frame,True))