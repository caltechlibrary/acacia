#!/usr/bin/env python3

#
# email_processor - this object is responsible for downloading the EMail
# from an account (e.g. submissions.authors@example.edu) and rendering
# them into a a database suitable for queuing production of EPrints XML
#
import os
import sys

from imaplib import IMAP4, IMAP4_SSL
import email

from peewee import Model, CharField, TextField, DateTimeField
from decouple import config

_db = config('DATABASE', 'acacia.db')

class Message(Model):
    msg_id = CharField(unique = True)
    msg_reply_to = CharField()
    msg_date = DateTimeField()
    msg_from = CharField()
    msg_subject = CharField()
    msg_body = TextField()

    class Meta():
        database = _db

def unquote(s):
    s = s.strip()
    if s.startswith("'"):
        return s.strip("'")
    elif s.startswith('"'):
        return s.strip('"')
    return s.strip()

class EMailProcessor():
    def __init__(self):
        self.imap_host = config('IMAP_HOST','')
        self.imap_port = config('IMAP_PORT', 993)
        self.smtp_host = config('SMTP_HOST', '')
        self.smtp_require_tls = config('STMP_REQUIRE_TLS', True)
        self.smtp_auth = config('SMTP_AUTH', True)
        self.smtp_ssl_port = config('SMTP_SSL_PORT', 465)
        self.smtp_tls_port = config('SMTP_TLS_PORT', 587)
        self.display_name = config('DISPLAY_NAME', '')
        self.email = config('EMAIL', '')
        self.secret = config('SECRET', '')

    def get_mail(self, smtp_dry_run = False):
        user = unquote(self.email)
        passwd = unquote(self.secret)
        if user == "":
            print(f'User not set.')
            return False
        if passwd == "":
            print(f'Password not set for {user}')
            return False
        print(f'Connect to {self.imap_host}:{self.imap_port} as {user}')
        if smtp_dry_run == True:
            print(f'Dry run. No connection made.')
            return True
        else:
            print(f'Making connection');
            M = IMAP4_SSL(self.imap_host, self.imap_port)
            try: 
                M.login(user, passwd)
            except Exception as err:
                print(f'Cannot connect, {err}')
                return False
            res, cnt = M.select()
            print(f'{res}, {cnt} message found')
            res, data = M.search(None, 'ALL')
            if res == 'OK':
                for num in data[0].split():
                    res, data = M.fetch(num, '(RFC822)')
                    if res == 'OK':
                        msg = email.message_from_bytes(data[0][1])
                        print(f'DEBUG msg({num}) -> {msg.as_string()}')
                    else:
                        print(f"Can't read message {num}")
            else:
                print('No messages')
                return False
            M.close()
            M.logout()
            return True
       
