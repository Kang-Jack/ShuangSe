#!/usr/bin/env python
# encoding: utf-8
"""
python_3_email_with_attachment.py
Created by Robert Dempsey on 12/6/14.
Copyright (c) 2014 Robert Dempsey. Use at your own peril.
This script works with Python 3.x
NOTE: replace values in ALL CAPS with your own values
"""
import sys
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '

def main():
    sender = 'wangxiao_1_2_3@sina.com'
    gmail_password = 'XXX'
    # recipients = ['EMAIL ADDRESSES HERE SEPARATED BY COMMAS']
    recipients = ['wangxiao_1_2_3@sina.com']
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'db'
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # List of attachments
    attachments = ['lottery.db']

    # Add the attachments to the message
    for file in attachments:
        try:
            print("open db")
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)
            print("attach db")
        except:
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            raise

    composed = outer.as_string()
    
    # Send the email
    try:
        print("smtplib")
        s = smtplib.SMTP('smtp.sina.com', 25)
        s.set_debuglevel(1)
        s.ehlo()
        s.starttls()
        s.ehlo()
        print("logging")
        s.login(sender, gmail_password)
        print("sending")
        s.sendmail(sender, recipients, composed)
        s.close()
        print("Email sent!")
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise

if __name__ == '__main__':
    main()
