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
from peewee import SqliteDatabase, Model
from peewee import CharField, TextField, DateTimeField, BooleanField

from . import cmds

_db = SqliteDatabase(config('DATABASE', 'acacia.db'))

# e.g. 'Wed, 15 Jul 2020 12:13:29 -0700'
dt_email_format = '%a, %d %b %Y %H:%M:%S %z'

def setup_message_table(db_name, table_name = 'message'):
    '''setup a SQLite3 database table'''
    db = SqliteDatabase(db_name)
    if db.connect():
        if db.table_exists(table_name):
            print(f'''WARNING: {table_name} already exists in {db_name}''')
        else:
            db.create_tables([Message])
            print(f'''{table_name} table created in {db_name}''')
    else:
        print(f'''ERROR: could not connect to {db_name}''')

def upgrade_message_table(db_name, table_name = 'message'):
    # Find upgrade sql file to run.
    sql_file = os.path.join('schema', f'upgrade_{table_name}.sql')
    if os.path.exists(sql_file):
        with open(sql_file, 'r') as fp:
            sql = fp.read()
    else:
        print(f'''ERROR: {sql_file} does not exist. Upgrade aborted''')
    # Copy existing SQLite3 database to a backup
    backup_name = f'{db_name}.bak-' + datetime.now().strftime('%Y%m%d%H%M%S')
    shutil.copyfile(db_name, backup_name)

    cmd = ["sqlite3", '--init', f'{sql_file}', db_name, '.exit' ]
    out, err = cmds.run(cmd)
    if err:
        print(f'''ERROR ({' '.join(cmd)}): {err}''')
        sys.exit(1)
    
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

