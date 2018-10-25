import numpy as np

debug = 0


class census_data:
    @staticmethod
    def get_red_matrix(data):
        count = len(data)
        if count < 1:
            return [[]]
        red_matrix = np.zeros((count, 34), dtype=np.int)
        for i in range(count):
            red_matrix[i][0] = data[i][0]
            for j in range(2, 8):  # Red balls in 2-7
                red_matrix[i][int(data[i][j])] = 1
        return red_matrix

    @staticmethod
    def get_blue_matrix(data):
        count = len(data)
        if count < 1:
            return [[]]
        blue_matrix = np.zeros((count, 17), dtype=np.int)
        for i in range(count):
            blue_matrix[i][0] = data[i][0]
            blue_matrix[i][int(data[i][8])] = 1
        return blue_matrix

    @staticmethod
    def get_date_id_map(data):
        count = len(data)
        if count < 1:
            return [[]]
        data_map = [[0, 0] for i in range(count)]
        for i in range(0, count):
            # data_map[i].append([data[i][0],data[i][1]])
            data_map[i][0] = data[i][0]
            data_map[i][1] = data[i][1]
        return data_map

    @staticmethod
    def calc_per(num, total):
        return float(num) / float(total) * 100

        # return "%.2f%%" % (float(num)/float(total)*100)

    @staticmethod
    def get_sum_info(df, is_blue):
        count = len(df.index)
        if count < 1:
            return
        max_n = 34
        if is_blue:
            max_n = 17
        append_data = [[0 for i in range(max_n)] for i in range(2)]
        # print append_data
        sum_n = 0
        for i in range(1, max_n):
            # if debug==1:print i
            append_data[0][i] = sum(df[i])
            sum_n = sum_n + append_data[0][i]
            append_data[1][i] = census_data.calc_per(append_data[0][i], count)
        # if debug==1:print sum_n
        return append_data

    @staticmethod
    def check_same_rate_blue(ballrates, is_blue):
        max_n = 33
        if is_blue:
            max_n = 16
        new = sorted(ballrates, reverse=False)
        max_diff = float(new[max_n]) - float(new[1])
        '''print ballrates
        if debug==1:print new
        if debug==1:print new[0]
        if debug==1:print new[1]
        if debug==1:print new[max_n]'''
        if debug == 1: print(max_diff)
        return max_diff < 6

    @staticmethod
    def find_same_rate_scale_blue(alldf):
        count = len(alldf.index)
        if count < 1:
            return [[]]
        # for i in range(2106,2108):
        for i in range(1859):
            end_index = i + 200
            if end_index < count:
                suminfo = census_data.get_sum_info(alldf[i:end_index], True)
                if census_data.check_same_rate_blue(suminfo[1], True):
                    if debug == 1: print('the scale is :' + str(i) + 'line')
