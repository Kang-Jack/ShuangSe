from pandas import DataFrame, Series
import pandas as pd
import numpy as np
from query_historical_data import historical_data
from census import census_data
debug = 1
historical_data = historical_data()
def get_blue_matrix_df ():
    rs=historical_data.get_all_data()
    return DataFrame(census_data.get_blue_matrix(rs))

def get_indexed_blue_matrix(blue_matrix_frame):
    df= blue_matrix_frame.loc[:,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]].cumsum()
    df[17]=blue_matrix_frame[0]
    df['index']=df.index
    return df

def get_historical_rounds(df):
    s=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    length= len(df)
    result=[]
    maxV=[]
    for i in range (length):
        rs = df.loc[i,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]].sub(s)
        if rs.min(axis=0)>0:
            s = df.loc[i]
            result.append(i)
            maxV.append(rs.max(axis=0))

    resultLen=[]
    length= len(result) 
    for i in range (length): 
        if i==0: resultLen.append(result[0]) 
        else: resultLen.append(result[i]-result[i-1])

    dfResult=DataFrame(result)
    dfResult['max']=maxV 
    dfResult['length']=resultLen 
    return dfResult

def get_historical_rounds_describe(dfResult):
    return dfResult[(dfResult['max']>3) & (dfResult['max'] <15)].describe()

def SumCurrentCol (df):
    return df.loc[:,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]].cumsum()
def GetBlueSumFrame(df,startRow,endRow):
    return SumCurrentCol(df.iloc[startRow:endRow])

def get_current_blue_frame(blue_matrix,start,end):
    return GetBlueSumFrame(blue_matrix_frame,start,end)

if __name__ == "__main__":

    if debug == 1: print ('===start===')
    
    blue_matrix_frame = get_blue_matrix_df ()

    df_indexed =  get_indexed_blue_matrix(blue_matrix_frame)
    
    blue_matrix_len =len(df_indexed)
    
    df_r = get_historical_rounds (df_indexed)
    
    start = df_r.loc[len(df_r)-1,0].astype(int)+1

    if debug == 1: print (df_r.values.tolist())
    
    df_r_des = get_historical_rounds_describe(df_r)
    
    if debug == 1: print (df_r_des.values.tolist())
    
    current_blue= get_current_blue_frame(blue_matrix_frame,start,blue_matrix_len)
    
    if debug == 1: print(current_blue.values.tolist())  
    if debug == 1: print ('===end===')