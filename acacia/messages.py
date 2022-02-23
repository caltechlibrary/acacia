#!/usr/bin/env python3

#
# email_processor - this object is responsible for downloading the EMail
# from an account (e.g. submissions.authors@example.edu) and rendering
# them into a a database suitable for queuing production of EPrints XML
#
import os
import sys
import shutil
from datetime import datetime

from imaplib import IMAP4, IMAP4_SSL
import email
from email.parser import BytesParser, Parser
from email.policy import default
from email.message import EmailMessage

from decouple import config

import pymysql
from peewee import MySQLDatabase, Model
from peewee import CharField, TextField, DateTimeField, BooleanField

from . import cmds

db_name = config('DATABASE_NAME', 'acacia')
db_host = config('DATABASE_HOST', 'localhost:3306')
if ':' in db_host:
    host, port = db_host.split(':', 2)
    if isinstance(port, str):
        port = int(port)
else:
    host = db_host
    port = 3306
db_user = config('DATABASE_USER', 'root')
db_password = config('DATABASE_PASSWORD', '')
_db = MySQLDatabase(db_name, host = host, port = port, user = db_user, password = db_password)


# e.g. 'Wed, 15 Jul 2020 12:13:29 -0700'
dt_email_format = '%a, %d %b %Y %H:%M:%S %z'

def setup_message_table(table_name = 'message'):
    '''setup a MySQL 8 database table'''
    if _db.connect():
        if _db.table_exists(table_name):
            print(f'''WARNING: {table_name} already exists in {db_name}''')
        else:
            _db.create_tables([Message])
            print(f'''{table_name} table created in {db_name}''')
    else:
        print(f'''ERROR: could not connect to {db_name}''')

def populate_field(key, msg, default = ''):
    field = None
    if key in msg:
        field = msg[key]
    else:
        field = default
    return field

def email_date_to_datetime(s):
    return None

class Message(Model):
    m_id = CharField(unique = True)
    m_reply_to = CharField()
    m_date = DateTimeField()
    m_to = CharField()
    m_from = CharField()
    m_subject = CharField()
    m_body = TextField()
    m_processed = BooleanField(null = False, default = False)
    # When was the record last updated
    updated = DateTimeField(default=datetime.now)
    # When the record was created
    created = DateTimeField(default=datetime.now)

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
        self.email = config('SUBMIT_EMAIL', '')
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
            (res, cnt) = M.select(readonly=True)
# Convert cnt to the integer it represents.
            if isinstance(cnt, list):
                cnt = cnt[0]
                if isinstance(cnt, bytes):
                    cnt = int(cnt)
            if cnt == 1:
                print(f'{res}, {cnt} message found')
            else:
                print(f'{res}, {cnt} messages found')
            res, data = M.search(None, 'ALL')
            if res == 'OK':
                for num in data[0].split():
                    res, data = M.fetch(num, '(RFC822)')
                    if res == 'OK':
                        msg = email.message_from_bytes(data[0][1], policy = default)
                        msg_id = populate_field('Message-ID', msg, None)
                        if msg_id:
                            now = datetime.now()
                            m = Message.get_or_none(m_id = msg_id)
                            if m == None:
                                m = Message()
                                m.m_id = msg_id
                                m.created = now
                            m.m_to = populate_field('To', msg, '')
                            m.m_reply_to = populate_field('Reply-To', msg, '')
                            m.m_from = populate_field('From', msg, '')
                            m.m_subject = populate_field('Subject', msg, '')
                            m.m_date = datetime.strptime(populate_field('Date', msg, None), dt_email_format)
                            m.m_body = msg.get_body(preferencelist=('plain', 'html'))
                            m.updated = now
                            m.save()
                        else:
                            print(f'ERROR: could not save {str(num)} {msg_id}, {m.m_subject}, {m.m_date}')
                    else:
                        print(f"Can't read message {num}")
            else:
                print('No messages')
                return False
            M.close()
            M.logout()
            return True
       
    def get_unprocessed(self):
        '''Returns an arrays of messages which are flagged as unprocessed.'''
        #records = [] 
        #for m in Message.select().where(Message.m_processed == False):
        #if m.m_body:
        #        records.append(m)
        #return records
        return Message.select().where(Message.m_processed == False)

    def cleanup_mailbox(self, smtp_dry_run = False):
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
            (res, cnt) = M.select(readonly=True)
# Convert cnt to the integer it represents.
            if isinstance(cnt, list):
                cnt = cnt[0]
                if isinstance(cnt, bytes):
                    cnt = int(cnt)
            if cnt == 1:
                print(f'{res}, {cnt} message found')
            else:
                print(f'{res}, {cnt} messages found')
            cleanup = False
            res, data = M.search(None, 'ALL')
            if res == 'OK':
                for num in data[0].split():
                    res, data = M.fetch(num, '(RFC822)')
                    if res == 'OK':
                        msg = email.message_from_bytes(data[0][1], policy = default)
                        msg_id = populate_field('Message-ID', msg, None)
                        if msg_id:
                            now = datetime.now()
                            m = Message.get_or_none(m_id = msg_id)
                            # remove message from messages table if found.
                            if (m != None) and (m.m_processed == 1):
                                cleanup = True
                                Message.delete().where(Message.m_id == msg_id).execute()
                                M.store(num, '+FLAGS', '\\Deleted')
                        else:
                            print(f'ERROR: could not find {str(num)} {msg_id}, {m.m_subject}, {m.m_date}')
                    else:
                        print(f"Can't read message {num}")
                if cleanup:
                    M.expunge()
            else:
                print('No stale messages')
                return False
            M.close()
            M.logout()
            # Clean up any lingering stale processed messages.
            Message.delete().where(Message.m_processed == 1).execute()
            return True
