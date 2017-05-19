from pandas import DataFrame, Series
import pandas as pd
import numpy as np
class matrix_data:
    @staticmethod
    def parse_red_balls(data):
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
    def parse_blue_ball(data):
        count=len(data)
        if count <1:
            return [[]]
        blue_matrix=np.zeros((count,17), dtype=np.int)
        for i in range (count):
            blue_matrix[i][0] = data[i][0]
            blue_matrix[i][int(data[i][8])] = 1
        return blue_matrix

    @staticmethod
    def parse_date_id_map(data):
        count=len(data)
        if count <1:
            return [[]]
        data_map= [[0,0] for i in range(count)]
        for i in range (0,count):
            #data_map[i].append([data[i][0],data[i][1]])
            data_map[i][0] = data[i][0]
            data_map[i][1] = data[i][1]
        return data_map
        