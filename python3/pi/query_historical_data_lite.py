import getopt
import sys

from pandas import DataFrame

#import dblottery
import db_lite as dblottery

debug = 1


class historical_data:
    db = dblottery.dblotterylite()

    def __init__(self):
        self.db = dblottery.dblotterylite()
    def get_one_year_data(self, year):
        data = []
        rows = self.db.query(r"SELECT * FROM doubleball where doubleball.GENERATE_TIME like '" + year + "%'")
        for row in rows:
            data.append(self.parse_row_data(row))
        if debug == 1: print(str(rows[0][0]))
        if debug == 1: print(rows[0][1].strip("\""))
        if debug == 1: print(rows[0][2].strip("\""))
        # if debug==1: print data
        return data

    def get_data_indentifier_range(self, year_begin, year_end):
        data = []
        rows = self.db.query(
            r"SELECT * FROM doubleball where doubleball.IDENTIFIER between " + year_begin + " and " + year_end)
        for row in rows:
            data.append(self.parse_row_data(row))
        if debug == 1: print(str(rows[0][0]))
        if debug == 1: print(rows[0][1].strip("\""))
        if debug == 1: print(rows[0][2].strip("\""))
        if debug == 1: print(str(rows[len(rows) - 1][0]).strip("\""))
        if debug == 1: print(rows[len(rows) - 1][1].strip("\""))
        if debug == 1: print(rows[len(rows) - 1][2].strip("\""))
        # if debug==1: print data
        return data

    def get_all_data(self):
        data = []
        rows = self.db.query(r"SELECT * FROM doubleball where 1=1 ")
        i=0
        for row in rows:
            if i == 0:
                i=i+1
                continue
            data.append(self.parse_row_data_lite(row))
        
        if debug == 1: print(str(rows[0][0]))
        if debug == 1: print(rows[0][1].strip("\""))
        if debug == 1: print(rows[0][2].strip("\""))
        if debug == 1: print(str(rows[len(rows) - 1][0]).strip("\""))
        if debug == 1: print(rows[len(rows) - 1][1].strip("\""))
        if debug == 1: print(rows[len(rows) - 1][2].strip("\""))
        return data

    def parse_row_data(self, row):
        print (row)
        return [row["IDENTIFIER"], row["GENERATE_TIME"].strip("\""), row["RED1"].strip("\""), \
                row["RED2"].strip("\""), row["RED3"].strip("\""), row["RED4"].strip("\""), \
                row["RED5"].strip("\""), row["RED6"].strip("\""), row["BLUE"].strip("\"")]
    
    def parse_row_data_lite(self, row):
        print (row)
        return [row[0], row[1].strip("\""), row[2].strip("\""), \
                row[3].strip("\""), row[4].strip("\""), row[5].strip("\""), \
                row[6].strip("\""), row[7].strip("\""), row[8].strip("\"")]

    def usage(self):
        print(r'Get all data by default')
        print(r'-s: Start of lottery No.')
        print(r'-e: End of  lottery No.')
        print(r'-y: Get single year data')
        print(r'-h: Help')


if __name__ == '__main__':
    historical_data = historical_data()
    opts, args = getopt.getopt(sys.argv[1:], 'hs:e:y:')
    csv_name = 'querycsv'
    startNo = ''
    endNo = ''
    singleY = ''
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
    if debug: print(startNo)
    if debug: print(endNo)
    if debug: print(singleY)
    rs = []
    if startNo != '' and endNo != '':
        rs = historical_data.get_data_indentifier_range(startNo, endNo)
        csv_name = startNo + '-' + endNo + '-data'
    elif singleY != '':
        rs = historical_data.get_one_year_data(singleY)
        csv_name = singleY + '-data'
    else:
        rs = historical_data.get_all_data()
        csv_name = 'ALL-data'
    df = DataFrame(rs)
    df.to_csv('./result/' + csv_name + '.csv', index=False)
    print(df)
