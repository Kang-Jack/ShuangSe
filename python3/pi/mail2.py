
# -*- coding: utf-8 -*-

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib
import pystache
import codecs
import time
import email, email.encoders, email.mime.text, email.mime.base
import email.mime.application
#import importlib,sys
#importlib.reload(sys)

#sys.setdefaultencoding('utf-8')


HOST = 'smtp.sina.cn'
PORT = 587
USER = 'wangxiao_1_2_3@sina.com'
PASS = 'xxxx'
FROM = 'wangxiao_1_2_3@sina.com'

SUBJECT = 'db'
HTML_NAME = 'tpl.html'
CSV_NAME = 'list.txt'
FAILED_LIST = []


def send(mail_receiver, mail_to):
    # text = mail_text
    html = render(mail_receiver)

    # msg = MIMEMultipart('alternative')
    msg = MIMEMultipart('mixed')
    msg['From'] = FROM
    msg['To'] = mail_to.encode()
    msg['Subject'] = SUBJECT.encode()

    # msg.attach(MIMEText(text, 'plain', 'utf-8'))
    msg.attach(MIMEText(html, 'html', 'utf-8'))

    # now attach the file
    #fileMsg = email.mime.base.MIMEBase('application', 'vnd.ms-excel')
    #fileMsg.set_payload(file('exelFile.xls').read())
    #email.encoders.encode_base64(fileMsg)
    #fileMsg.add_header('Content-Disposition', 'attachment;filename=anExcelFile.xls')
    #msg.attach(fileMsg)

    filename = 'lottery.db'
    fp = open(filename, 'rb')
    att = email.mime.application.MIMEApplication(fp.read(), _subtype="db")
    fp.close()
    att.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(att)


    try:
       # _sender = smtplib.SMTP(
       # #    HOST,
       # #    PORT
       # #)
        _sender = smtplib.SMTP()
        _sender.connect(HOST, 25) # 25 为 SMTP 端口号
        _sender.set_debuglevel(1)
        _sender.ehlo()
        _sender.starttls()
        _sender.ehlo()
        #_sender.starttls()
        _sender.login(USER, PASS)
        _sender.sendmail(FROM, mail_to, msg.as_string())
        _sender.quit()
        print ("Success")
    except smtplib.SMTPException as e:
        print (e)
        FAILED_LIST.append(mail_receiver + ',' + mail_to)


def render(name):
    _tpl = codecs.open(
        './html/' + HTML_NAME,
        'r',
        'utf-8'
    )
    _html_string = _tpl.read()
    return pystache.render(_html_string, {
        'receiver': name
    })


def main():
    #ls = open('./csv/' + CSV_NAME, 'r')
    mail_list =['wangxiao_1_2_3@sina.com,wangxiao_1_2_3@sina.com'] #ls.read().split('\r')

    for _receiver in mail_list:
        _tmp = _receiver.split(',')
        print ('Mail: ' + _tmp[0] + ',' + _tmp[1])
        time.sleep(20)
        send(_tmp[0], _tmp[1])

    print (FAILED_LIST)
if __name__ == "__main__":

    debug = 1
    main()