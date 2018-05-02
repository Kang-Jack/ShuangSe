import csv
import datetime
import getopt
import re
import sys
import urllib.request
import chardet
import zlib


type = sys.getfilesystemencoding()

from bs4 import BeautifulSoup

# dblottery
import db_lite as dblottery

debug = 1


def handleRedBalls(redballs):
    lenballs = len(redballs)
    if lenballs == 6:
        strball = str(
            redballs[0] + ',' + redballs[1] + ',' + redballs[2] + ',' + redballs[3] + ',' + redballs[4] + ',' +
            redballs[5])
    return strball


def handleBlueBalls(blueballs):
    lenballs = len(blueballs)
    if lenballs == 1:
        strball = str(blueballs[0])
    return strball


def saveNewData2CSV(csvFile, limit):
    writer = csv.writer(csvFile)
    # output = file('2016-2017data.txt', 'w+')
    # req_html_doc = requests.get("http://baidu.lecai.com/lottery/draw/list/50?type=range&start="+startNo+"&end="+endNo).text
    my_soup = fetch_page_content(limit)
    result = my_soup.findAll('tr')
    for each in result:
        # parse Lottery SN
        lottery_qihao = parse_qihao(each)
        if len(lottery_qihao) != 0:
            if debug: print (lottery_qihao)
            # parse date
            lottery_date = parse_date_info(each)
            # parse red balls
            lottery_haoma_red = parse_red_balls(each)
            # parse blue ball
            lottery_haoma_blue = parse_blue_balls(each)
            # if len(lottery_qihao) != 0:
            insert_to_csv(lottery_date, lottery_haoma_blue, lottery_haoma_red, lottery_qihao, writer)
            # out_line = str(lottery_date) + lottery_qihao[0][1] + str(lottery_haoma_red) + str(lottery_haoma_blue) + '\n'
            # output.write(out_line)


def insert_to_csv(lottery_date, lottery_haoma_blue, lottery_haoma_red, lottery_qihao, writer):
    writer.writerow((
        "20" + lottery_qihao[0], handleRedBalls(lottery_haoma_red), handleBlueBalls(lottery_haoma_blue),
        str(lottery_date[0])))


def saveNewData2DB(limit):
    db = dblottery.dblotterylite()
    # output = file('2016-2017data.txt', 'w+')
    my_soup = fetch_page_content(limit)
    result = my_soup.findAll('tr')
    i = 0
    for each in result:
        # parse Lottery SN
        lottery_qihao = parse_qihao(each)
        if len(lottery_qihao) != 0:
            if debug: print (lottery_qihao)
            # parse date
            lottery_date = parse_date_info(each)
            # parse red balls
            lottery_haoma_red = parse_red_balls(each)
            # parse blue ball
            lottery_haoma_blue = parse_blue_balls(each)
            # writer.writerow((lottery_qihao[0][1],handleRedBalls(lottery_haoma_red),handleBlueBalls(lottery_haoma_blue),str(lottery_date[0])))
            rs = insert_to_db(db, lottery_date, lottery_haoma_blue, lottery_haoma_red, lottery_qihao)
            if (rs == 1):
                i = i + 1
    if debug: print (i)
    return i



def insert_to_db(db, lottery_date, lottery_haoma_blue, lottery_haoma_red, lottery_qihao):
    db.insert_doubleball(int("20" + lottery_qihao[0]), str(lottery_date[0]), str(lottery_haoma_red[0]),
                         str(lottery_haoma_red[1]), str(lottery_haoma_red[2]), str(lottery_haoma_red[3]),
                         str(lottery_haoma_red[4]), str(lottery_haoma_red[5]), str(lottery_haoma_blue[0]))


def fetch_page_content(limit):
    # http://datachart.500.com/ssq/history/newinc/history.php?limit=5
    # http://datachart.500.com/ssq/history/newinc/history.php?start=17090&end=17096
    print("http://datachart.500.com/ssq/history/newinc/history.php")
    req = urllib.request.Request("http://datachart.500.com/ssq/history/newinc/history.php?limit="+str(limit)+"&sort=0")
    print ("http://datachart.500.com/ssq/history/newinc/history.php?limit="+str(limit)+"&sort=0")
    with urllib.request.urlopen(req) as response:
        req_html_doc = response.read()
        req_html_doc = zlib.decompress(req_html_doc, 16 + zlib.MAX_WBITS)
        print(chardet.detect(req_html_doc))
        #req_html_doc=str(response.read(), 'windows-1252')
        #req_html_doc = unicode(req_html_doc, 'GBK').encode('UTF-8')
    my_soup = BeautifulSoup(req_html_doc, "html5lib")
    print (my_soup.original_encoding)
    return my_soup


def parse_qihao(each):
    reg_lottery_qihao = re.compile(r'<td>(\d{5})</td>')
    lottery_qihao = reg_lottery_qihao.findall(str(each))
    return lottery_qihao


def parse_blue_balls(each):
    bs_lottery_haoma_blue = each.findAll('td', {"class": "t_cfont4"})
    reg_lottery_haoma_blue = re.compile(r'>([0-9]*)</td>')
    lottery_haoma_blue = reg_lottery_haoma_blue.findall(str(bs_lottery_haoma_blue))
    if debug: print(bs_lottery_haoma_blue)
    if debug: print(lottery_haoma_blue)
    return lottery_haoma_blue


def parse_red_balls(each):
    bs_lottery_haoma_red = each.findAll('td', {"class": "t_cfont2"})
    reg_lottery_haoma_red = re.compile(r'>([0-9]*)</td>')
    lottery_haoma_red = reg_lottery_haoma_red.findall(str(bs_lottery_haoma_red))
    if debug: print(bs_lottery_haoma_red)
    if debug: print(lottery_haoma_red)
    return lottery_haoma_red


def parse_date_info(each):
    reg_lottery_date = re.compile(r'<td>(\d{4}-\d{2}-\d{2}.*)</td>')
    re_date = re.compile(r'\d{4}-\d{2}-\d{2}')
    y_date = reg_lottery_date.findall(str(each))
    lottery_date = re_date.findall(str(y_date))
    if debug: print(lottery_date)
    return lottery_date


def usage():
    print (r'-l: fetch limit recorder No. ')
    print (r'-h: Help')


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], 'hl:')
    now = datetime.datetime.now()
    startNo = str(now.year) + '001'
    endNo = str(now.year) + '160'
    limit = '50'
    for op, value in opts:
        if op == "-l":
            limit = value
        elif op == "-h":
            usage()
            sys.exit()
    saveNewData2DB(limit)
    '''csvFile = file(startNo+'-'+endNo+'data.csv', 'w+')
    try:
        saveNewData2CSV(csvFile,startNo,endNo)
    except Exception,e:  
        print Exception,":",e
    finally:
        csvFile.close()'''