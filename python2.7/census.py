from pandas import DataFrame, Series
import pandas as pd
import numpy as np
debug =1

class census_data:
    @staticmethod
    def get_red_matrix(data):
        count=len(data)
        if count <1:
            return [[]]
        red_matrix=np.zeros((count,34), dtype=np.int)
        for i in range (count):
            red_matrix[i][0] = data[i][0]
            for j in range(2,8): # Red balls in 2-7 
                red_matrix[i][int(data[i][j])] = 1
        return red_matrix

    @staticmethod
    def get_blue_matrix(data):
        count=len(data)
        if count <1:
            return [[]]
        blue_matrix=np.zeros((count,17), dtype=np.int)
        for i in range (count):
            blue_matrix[i][0] = data[i][0]
            blue_matrix[i][int(data[i][8])] = 1
        return blue_matrix

    @staticmethod
    def get_date_id_map(data):
        count=len(data)
        if count <1:
            return [[]]
        data_map= [[0,0] for i in range(count)]
        for i in range (0,count):
            #data_map[i].append([data[i][0],data[i][1]])
            data_map[i][0] = data[i][0]
            data_map[i][1] = data[i][1]
        return data_map

    @staticmethod
    def calc_per(num,total):
        return (float(num)/float(total)*100)

        #return "%.2f%%" % (float(num)/float(total)*100)

    @staticmethod
    def get_sum_info (df,isBlue):
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
            #if debug==1:print i
            append_data[0][i] = sum(df[i])
            sumN=sumN+append_data[0][i]
            append_data[1][i] = census_data.calc_per(append_data[0][i],count)
        #if debug==1:print sumN
        return append_data
    @staticmethod
    def check_same_rate_blue(ballrates,isBlue):
        maxN = 33
        if isBlue :
            maxN=16
        new = sorted(ballrates,reverse=False)
        maxDiff = float(new[maxN])-float(new[1])
        '''print ballrates
        if debug==1:print new
        if debug==1:print new[0]
        if debug==1:print new[1]
        if debug==1:print new[maxN]'''
        if debug==1:print maxDiff
        return maxDiff<2

    @staticmethod
    def find_same_rate_scale_blue(alldf):
        count = len(alldf.index)
        if count <1:
            return [[]]
        #for i in range(2106,2108):
        for i in range(1359):
            endIndex=i+1000
            if endIndex < count: 
                suminfo = census_data.get_sum_info(alldf[i:endIndex],True)
                if census_data.check_same_rate_blue(suminfo[1],True) :
                    print 'the scale is :' +str(i) +'line'

        