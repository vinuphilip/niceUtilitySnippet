#!/usr/bin/python

import imaplib
import getpass
import sys
import base64
from Crypto.Cipher import AES


'''
usage: python gmailDeleteEmails.py  fileNameList='listOfKeywordsToBeDeleted'  username='username' -- if you dont want to get it prompted
'''

username = raw_input("Enter your GMail username:")
pwd = getpass.getpass("Enter your password: ")


# encryption logic

#e_b64_cipher_text = "Put your base64 encoded pwd here"
#d_b64_cipher_text = base64.b64decode(e_b64_cipher_text)

# Decryption
#decryption_suite = AES.new('put your 16 char key here', AES.MODE_ECB)
#plain_text = decryption_suite.decrypt(d_b64_cipher_text)
#pwd =  plain_text.strip()


args = dict([arg.split('=') for arg in sys.argv[1:]])


#print ("Logging into gmail using user %s\n" %args['username'])
print ("Logging into gmail using user %s\n" %username)

imapServerConnection = imaplib.IMAP4_SSL('imap.gmail.com')

#imapServerConnectionMessage = imapServerConnection.login(args['username'], pwd)
imapServerConnectionMessage = imapServerConnection.login(username, pwd)
print(imapServerConnectionMessage)

#print("possible lists are as below")
#print imapServerConnection.list()

print ("using Inbox")
imapServerConnection.select("inbox")

with open(args['fileNameList'],'r') as f:
    for sender in f:
        sender = sender.strip()
        #print ("searching mails from user %s " % args['sender'])
        print ("searching mails from user %s " % sender)

        result_status, email_ids = imapServerConnection.search(None, '(FROM "%s")' % sender)
        #result_status, email_ids = imapServerConnection.search(None, '(FROM "%s")' % args['sender'])
        #result_status, email_ids = imapServerConnection.search(None, '(FROM ladder")')

        email_ids =  email_ids[0].split()

        if len(email_ids) == 0:
            print ("no emails found ......finishing")
        else:
            print("Found %d email or emails from user %s , moving to thrash" % (len(email_ids),sender))

        for emailItems in email_ids:
            print("moving %s" % emailItems)
            imapServerConnection.store(emailItems, '+X-GM-LABELS', '\\Trash')
    
imapServerConnection.expunge()

print("Done ........")


