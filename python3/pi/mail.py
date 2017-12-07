# Import smtplib for the actual sending function
import smtplib

# For guessing MIME type
import mimetypes

# Import the email modules we'll need
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email.mime.application
class sina_mail(object):
    def __init__(self):
        # Create a text/plain message
        self.msg = email.mime.multipart.MIMEMultipart()
        self.msg['Subject'] = 'db'
        self.msg['From'] = 'wangxiao_1_2_3@sina.com'
        self.msg['To'] = 'wangxiao_1_2_3@sina.com'
    def send(self):
        # The main body is just another attachment
        body = email.mime.text.MIMEText("""Hello, how are you? I am fine.
        This is a rather nice letter, don't you think?""")
        self.msg.attach(body)

        # PDF attachment
        #filename='lottery.db'
        #fp=open(filename,'rb')
        #att = email.mime.application.MIMEApplication(fp.read(),_subtype="db")
        #fp.close()
        #att.add_header('Content-Disposition','attachment',filename=filename)
        #self.msg.attach(att)

        # send via sina server
        # NOTE: my ISP, Centurylink, seems to be automatically rewriting
        # port 25 packets to be port 587 and it is trashing port 587 packets.
        # So, I use the default port 25, but I authenticate.

        s = smtplib.SMTP('smtp.sina.com')
        s.set_debuglevel(1)
        #s.ehlo()
        s.starttls()
        #s.ehlo()
        s.login('wangxiao_1_2_3@sina.com','xxxx')
        s.sendmail('wangxiao_1_2_3@sina.com',['wangxiao_1_2_3@sina.com'], self.msg.as_string())
        s.quit()
        print ("Success")
if __name__ == "__main__":

    debug = 1
    mail=sina_mail()
    mail.send()