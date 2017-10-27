from __future__ import division

import numpy as np
from pandas import DataFrame

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
    def calc_probability (df,max_show,trust_num):
        MaxShow=max_show    # Max show time in Trust Zone
        TrustNum=trust_num  # define Trust Zone scope
        sumShows=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]  # record summary of show times for each col
        #get summary of current col
        #SumCol= SumCurrentCol(Col)             
        # update record 
        initRate=(1/16)*(1/TrustNum)*100
        initTempR=[initRate for i in range(16)]
        rs=[initTempR]

        dfLength= len(df)
        row=df[0:1]
        if debug==1:print (dfLength)
        if debug==1:print (row)
        #remove table head
        for i in range (dfLength): 
            if i<1:
                continue
            else:
                row =df[i-1:i]
            if debug==1:print ("row:")
            if debug==1:print (row)
            sumShows = row.values[0]       
            tempR=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
            if debug==1:print (i)
            if debug==1:print (sumShows)
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
                if debug==1:print (tempR[j])
            rs.append(tempR)
        return rs

    @staticmethod
    def get_probability_matrix (df,dfCensusResult): 
        census_length=len(dfCensusResult)
        row =dfCensusResult[0:1]
        previous_line=0
        rs=[[]]
        for i in range (census_length+1):
            if i == 0:
                continue
            row =dfCensusResult[i-1:i]
            end_line= row[0].values[0]+1
            df3 = analyze_blue.get_blue_sum_frame(df,previous_line,end_line)
            #df3 =analyze_blue.analyze_blue.get_blue_sum_frame(blue_matrix_frame,0,105)
            if debug==1:print (row['max'].values[0].astype(int))
            if debug==1:print (row['length'].values[0])
            temp_rs = analyze_blue.calc_probability(df3,row['max'].values[0].astype(int),row['length'].values[0])
            if i==1:
                rs=temp_rs
            else :
                rs=np.concatenate((rs, temp_rs))
            previous_line=end_line
        return rs

if __name__ == '__main__':
    import dblottery
    from query_historical_data import historical_data
    from census import census_data
    db = dblottery.dblottery()

    historical_data=historical_data()
    rs=historical_data.get_all_data()
    blue_matrix_frame = DataFrame(census_data.get_blue_matrix(rs))

    df= blue_matrix_frame.loc[:,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]].cumsum()
    df[17]=blue_matrix_frame[0]
    df['index']=df.index
    df.to_csv('summaryBlue.csv',index=False)
    dfCensusResult= analyze_blue.get_blue_census(df)
    #print dfCensusResult
    rs = analyze_blue.get_probability_matrix(blue_matrix_frame,dfCensusResult)

    rs_df=DataFrame(rs)
    rs_df['IDENTIFIER']=df[17]
    #print rs_df
    #rs_df.to_csv('CensusBlue.csv',index=False)