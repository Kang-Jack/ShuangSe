
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
from email.mime.application import MIMEApplication
from email import encoders
#from base64 import encodebytes

class sina_mail(object):
    def __init__(self):
        self.HOST = 'smtp.sina.com'
        self.PORT = 25
        self.USER = 'wangxiao_1_2_3@sina.com'
        self.PASS = 'raspberry-pi2'
        self.FROM = 'wangxiao_1_2_3@sina.com'

        self.SUBJECT = 'db'
        self.CSV_NAME = 'list.txt'
        self.FAILED_LIST = []

    def smtp_sender(self,mail_to):
        # msg = MIMEMultipart('alternative') #when alternative: no attach, but only plain_text
        msg = MIMEMultipart()
        msg['From'] = self.FROM
        msg['To'] = mail_to.encode()
        msg['Subject'] = 'db_'+str(time.time())
        body = MIMEText("""Hello, how are you? I am fine.
              This is a rather nice letter, don't you think?""")
        msg.attach(body)

    # attachment 
        fn = 'lottery.db'
        my_mimetype, encoding = mimetypes.guess_type(fn)
        print (my_mimetype, encoding)
        if my_mimetype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            my_mimetype = 'application/octet-stream'

        maintype, subtype = my_mimetype.split('/', 1) # split only at the first '/'
        print (maintype, subtype)
        if maintype == 'text':
            with open(fn,'rb') as fp:  # 'rb' will send this error: 'bytes' object has no attribute 'encode'
                # Note: we should handle calculating the charset
                attachement = MIMEText(fp.read(), _subtype=subtype)
                fp.close()
        elif maintype == 'image':
            with open(fn, 'rb') as fp:
                attachement = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
        elif maintype == 'audio':
            with open(fn, 'rb') as fp:
                attachement = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
        elif maintype == 'application' and subtype == 'pdf':
            with open(fn, 'rb') as fp:
                attachement = MIMEApplication(fp.read(), _subtype=subtype)
                fp.close()
        else:
            with open(fn, 'rb') as fp:
                attachement = MIMEApplication(fp.read(), _subtype='db')
                #attachement = MIMEBase(maintype, subtype)
                #attachement.set_payload(encodebytes(fp.read()).decode())
                #attachement.set_payload(fp.read())
                #fp.close()
        # Encode the payload using Base64
        #encoders.encode_base64(attachement)
        # Set the filename parameter
        #attachement.add_header('Content-Transfer-Encoding', 'base64')
        #fname = os.path.basename(fn)
        attachement.add_header('Content-Disposition', 'attachment', filename=os.path.basename(fn))
        msg.attach(attachement)
        #print (attachement)
        # Now send or store the message
        #composed = msg.as_string()

    
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
            _sender.sendmail(self.FROM, mail_to,msg.as_string())
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