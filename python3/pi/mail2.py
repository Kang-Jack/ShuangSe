
# -*- coding: utf-8 -*-

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib
import os

import mimetypes
import time
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email import encoders
from base64 import encodebytes

class sina_mail(object):
    def __init__(self):
        self.HOST = 'smtp.sina.com'
        self.PORT = 25
        self.USER = 'wangxiao_1_2_3@sina.com'
        self.PASS = 'xxxx'
        self.FROM = 'wangxiao_1_2_3@sina.com'

        self.SUBJECT = 'db'
        self.CSV_NAME = 'list.txt'
        self.FAILED_LIST = []

    def smtp_sender(self,mail_to):
        # msg = MIMEMultipart('alternative')
        msg = MIMEMultipart()
        msg['From'] = self.FROM
        msg['To'] = mail_to.encode()
        msg['Subject'] = 'db_'+str(time.time())
        body = MIMEText("""Hello, how are you? I am fine.
              This is a rather nice letter, don't you think?""")
        msg.attach(body)

        # now attach the file
        #fileMsg = email.mime.base.MIMEBase('application', 'vnd.ms-excel')
        #fileMsg.set_payload(file('exelFile.xls').read())
        #email.encoders.encode_base64(fileMsg)
        #fileMsg.add_header('Content-Disposition', 'attachment;filename=anExcelFile.xls')
        #msg.attach(fileMsg)


        # 构造MIMEBase对象做为文件附件内容并附加到根容器
        filename = 'lottery.db'
        ctype, encoding = mimetypes.guess_type(filename)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        if maintype == 'text':
            with open(filename) as fp:
                # Note: we should handle calculating the charset
                msg = MIMEText(fp.read(), _subtype=subtype)
        elif maintype == 'image':
            with open(filename, 'rb') as fp:
                msg = MIMEImage(fp.read(), _subtype=subtype)
        elif maintype == 'audio':
            with open(filename, 'rb') as fp:
                msg = MIMEAudio(fp.read(), _subtype=subtype)
        else:
            with open(filename, 'rb') as fp:
                msg = MIMEBase(maintype, subtype)
                msg.set_payload(fp.read())
            # Encode the payload using Base64
            encoders.encode_base64(msg)
        # Set the filename parameter
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(msg)

        # Now send or store the message
        composed = msg.as_string()






        #ctype, encoding = mimetypes.guess_type(filename)
        #if ctype is None or encoding is not None:
        #    ctype = 'application/octet-stream'
        #maintype, subtype = ctype.split('/', 1)

        #file_msg = email.mime.base.MIMEBase(maintype, subtype)

        #data = open(filename, 'rb')
        #file_msg.set_payload(data.read())
        #data.close()
        #email.encoders.encode_base64(file_msg)

        #print (ctype, encoding)

        #fp = open(filename, 'rb')
        #part = email.mime.base.MIMEBase('application', "octet-stream")
        #part.set_payload(encodebytes(fp.read()).decode())
        #fp.close()
        #part.add_header('Content-Transfer-Encoding', 'base64')
        #part.add_header('Content-Disposition', 'attachment; filename="%s"' % filename)
        #msg.attach(part)  # msg is an instance of MIMEMultipart()

        #msg.attach(file_msg)


        ## 设置附件头
        #basename = os.path.basename(filename)
        #file_msg.add_header('Content-Disposition', 'attachment', filename=basename)  # 修改邮件头
        #.attach(file_msg)


        try:
            _sender = smtplib.SMTP()
            _sender.connect(self.HOST, self.PORT) # 25 为 SMTP 端口号
            _sender.set_debuglevel(1)
            _sender.ehlo()
            _sender.starttls()
            _sender.ehlo()
            #_sender.starttls()
            _sender.login(self.USER, self.PASS)
            #_sender.sendmail(self.FROM, mail_to, msg.as_string())
            _sender.sendmail(self.FROM, mail_to,composed)
            _sender.quit()

            print ("Success")
        except smtplib.SMTPException as e:
            print (e)
            self.FAILED_LIST.append(mail_to)

    def send_db(self):
        #ls = open('./csv/' + CSV_NAME, 'r')
        mail_list =['wangxiao_1_2_3@sina.com'] #ls.read().split('\r')

        for _receiver in mail_list:
            print ('Mail: ' + _receiver)
            time.sleep(20)
            self.smtp_sender(_receiver)

        print (self.FAILED_LIST)
        return self.FAILED_LIST
if __name__ == "__main__":

    debug = 1
    mail= sina_mail()
    mail.send_db()