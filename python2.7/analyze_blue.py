from __future__ import division
import time
from pandas import DataFrame, Series
import pandas as pd
import numpy as np
debug =0

class analyze_blue:
    @staticmethod
    def get_blue_census(df):
        s=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        length= len(df)
        result=[]
        maxV=[]
        # Calc rounds of Trust zone,Max show time of each zone
        for i in range (length):
            rs = df.loc[i,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]].sub(s)
            if rs.min(axis=0)>0:
                s = df.loc[i]
                result.append(i)
                maxV.append(rs.max(axis=0))
        # Calc length if each zone
        resultLen=[]
        length= len(result) 
        for i in range (length): 
            if i==0: resultLen.append(result[0]) 
            else: resultLen.append(result[i]-result[i-1])
        dfResult=DataFrame(result)
        dfResult['max']=maxV 
        dfResult['length']=resultLen
        return dfResult

    #@staticmethod
   # def sum_current_col (df):
   #     return df.loc[:,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]].cumsum()
    
    @staticmethod
    def get_blue_sum_frame(df,startRow,endRow):
         rs_df = df.iloc[startRow:endRow]
         return rs_df.loc[:,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]].cumsum()

    @staticmethod
    def count_non_show_num(sumShows):
        length=len(sumShows)
        rs=length
        for i in range (length):
            if sumShows[i] > 0: rs=rs-1
        return rs

    @staticmethod
    def count_avliable_num(sumShows,maxShowTime):
        length=len(sumShows)
        rs=length
        for i in range (length):
            if sumShows[i] >= maxShowTime: rs=rs-1
        return rs

    @staticmethod
    def calc_probability (df):
        MaxShow=6    # Max show time in Trust Zone
        TrustNum=55  # define Trust Zone scope
        sumShows=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]  # record summary of show times for each col
        #get summary of current col
        #SumCol= SumCurrentCol(Col)             
        # update record 
        initRate=(1/16)*(1/TrustNum)*100
        initTempR=[initRate for i in range(16)]
        rs=[initTempR]

        dfLength= len(df)
        row=df[0:1]
        if debug==1:print dfLength
        if debug==1:print row
        #remove table head
        for i in range (dfLength): 
            if i<1:
                continue
            else:
                row =df[i-1:i]
            if debug==1:print "row:"
            if debug==1:print row
            sumShows = row.values[0]       
            tempR=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
            if debug==1:print i
            if debug==1:print sumShows
            for j in range(16):
                sumShow = sumShows[j]
                #print sumShow
                if sumShow > MaxShow:
                    tempR[j]=0
            # get number of zero in summary record 
                NonShow = analyze_blue.count_non_show_num(sumShows)
                #print NonShow
                if (TrustNum - i)> NonShow :
                    # get number of col not reached Maxshow times
                    avliableNum=analyze_blue.count_avliable_num(sumShows,MaxShow)
                    #print (1/avliableNum)*((MaxShow-sumShow)/MaxShow)*(1/(TrustNum - i)) #(1/(17-avliableNum))*
                    tempR[j]=(1/avliableNum)*((MaxShow-sumShow)/MaxShow)*(1/(TrustNum - i))*100
                    #print tempR[j]
                else:
                    #print "NonShow"
                    if sumShow ==0:
                        tempR[j]=(1/NonShow)*100
                    else :
                        tempR[j]=0
                if debug==1:print tempR[j]
            rs.append(tempR)
        return rs