# -*- coding:utf-8 -*-
from email.mime.text import MIMEText
import poplib
import smtplib


class MailManager(object):

    def __init__(self):
        self.popHost = 'pop.sina.com'
        self.smtpHost = 'smtp.sina.com'
        self.port = 25
        self.userName = 'wangxiao_1_2_3@sina.com'
        self.passWord = 'ati8500'
        self.bossMail = 'wangxiao_1_2_3@sina.com'
        #self.login()
        self.configMailBox()

        # 登录邮箱

    def login(self):
        try:
            self.mailLink = poplib.POP3_SSL(self.popHost,'25')
            self.mailLink.set_debuglevel(0)
            self.mailLink.user(self.userName)
            self.mailLink.pass_(self.passWord)
            self.mailLink.list()
            print(u'login success!')
        except Exception as e:
            print(u'login fail! ' + str(e))
            quit()

            # 获取邮件

    def retrMail(self):
        try:
            mail_list = self.mailLink.list()[1]
            if len(mail_list) == 0:
                return None
            mail_info = mail_list[0].split(' ')
            number = mail_info[0]
            mail = self.mailLink.retr(number)[1]
            self.mailLink.dele(number)

            subject = u''
            sender = u''
            for i in range(0, len(mail)):
                if mail[i].startswith('Subject'):
                    subject = mail[i][9:]
                if mail[i].startswith('X-Sender'):
                    sender = mail[i][10:]
            content = {'subject': subject, 'sender': sender}
            return content
        except Exception as e:
            print(str(e))
            return None

    def configMailBox(self):
        try:
            self.mail_box = smtplib.SMTP(self.smtpHost, self.port)
            self.mail_box.login(self.userName, self.passWord)
            print(u'config mailbox success!')
        except Exception as e:
            print(u'config mailbox fail! ' + str(e))
            quit()

            # 发送邮件

    def sendMsg(self, mail_body='Success!'):
        try:
            msg = MIMEText(mail_body, 'plain', 'utf-8')
            msg['Subject'] = mail_body
            msg['from'] = self.userName
            self.mail_box.sendmail(self.userName, self.bossMail, msg.as_string())
            print(u'send mail success!')
        except Exception as e:
            print(u'send mail fail! ' + str(e))


if __name__ == '__main__':
    mailManager = MailManager()
    mail = mailManager.retrMail()
    if mail != None:
        print(mail)
        mailManager.sendMsg()