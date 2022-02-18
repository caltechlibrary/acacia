#!/usr/bin/env python3

#
# doi.py is responsible for converting a stored (email) message
# include a series of retrival records (one per doi).  DOI retrieval
# records can then be aggregated to generate EPrintXML as well as a
# list of PDF urls to retrieve before importing into EPrints.
#
import os
import sys
import shutil
from datetime import datetime
from urllib.parse import urlparse

import idutils

from decouple import config

import pymysql
from peewee import MySQLDatabase, Model, Field
from peewee import CharField, IntegerField, TextField, DateTimeField, BooleanField

from . import cmds

doi2eprintxml_cmd = config('DOI2EPRINTXML', 'doi2eprintxml')
doi2eprintxml_email = config('DOI2EPRINTXML_EMAIL', '')

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

repo_id = config('REPO_ID', 'lemurprints')

# e.g. 'Wed, 15 Jul 2020 12:13:29 -0700'
dt_email_format = '%a, %d %b %Y %H:%M:%S %z'

def validate_doi(doi):
    return idutils.is_doi(doi)

def setup_doi_table(table_name = 'doi'):
    '''setup a MySQL 8 database table'''
    if _db.connect():
        if _db.table_exists(table_name):
            print(f'''WARNING: {table_name} already exists in {db_name}''')
        else:
            _db.create_tables([Doi])
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

workflow_states = [ 'pending', 'processing_error', 'ready', 'trash' ]

class Workflow(Field):
    field_type = 'workflow'

    def db_value(self, value):
        val = workflow_states[0]
        if value in workflow_states:
            val = value
        return val

    def python_value(self, value):
        val = workflow_states[0]
        if value in workflow_states:
            val = value
        return val

class Doi(Model):
    # doi is the only required field
    doi = CharField(unique = True)
    # object_url is the URL to the PDF or digital object related to the DOI
    object_url = CharField(default = '')
    # message id used for submission (if submitted via email)
    m_id = CharField(default = '')
    # message from used for submission (if submitted via email)
    m_from = CharField(default = '')
    # Workflow status
    status = CharField(default = 'unprocessed') # Workflow(default = 'unprocessed')
    # bundle-name, this is a machine generated associated with a download
    bundle_name = CharField(default = '')
    # EPrint XML for metadata retrieved from either CrossRef or DataCite
    # structure id based `doi2eprintxml DOI`
    metadata = TextField(default = '')
    # Any processing notes
    notes = TextField(default = '')
    # When was the record last updated
    updated = DateTimeField(default=datetime.now)
    # When the record was created
    created = DateTimeField(default=datetime.now)
    # EPrints eprint_id if known
    eprint_id = IntegerField(default = 0)
    # EPrints repository id if known
    repo_id = CharField(default = repo_id)

    class Meta():
        database = _db

def unquote(s):
    s = s.strip()
    if s.startswith("'"):
        return s.strip("'")
    elif s.startswith('"'):
        return s.strip('"')
    return s.strip()

def extract_doi_and_url(s):
    doi, url = None, None
    if '|' in s:
        p = s.split('|', maxsplit= 2)
        doi, url = p[0], p[1]
    elif idutils.is_doi(s):
        doi = s
    errors = [] 
    # clieanup doi
    if isinstance(doi, str):
        if doi.startswith('http://doi.org/'):
            doi = doi[len('http://doi.org/'):]
        elif doi.startswith('https://doi.org/'):
            doi = doi[len('https://doi.org/'):]
        if ('<' in doi) and doi.endswith('>'):
            doi, junk = doi.split('<', maxsplit=2)
        doi = doi.strip()
    # validate we have a DOI and URL
    if (doi != None) and (idutils.is_doi(doi) == False):
        errors.append(f'"{doi}" does not appear to be a DOI')
    # valudate URL is present
    is_url, uerr = True, ''
    try:
        u = urlparse(url)
    except Exception as err:
        is_url = False
    if (url != None) and (is_url == False):
        errors.append(f'"{url}" does not appear to be a URL, {uerr}')
    if len(errors) > 0:
        return doi, url, ', '.join(errors)
    return doi, url, None

class DOIProcessor:
    '''An object for working with Doi module.'''
    def __init__(self):
       self.db_name = _db
       self.table_name = 'doi'

    def message_to_doi(self, m, dry_run = False):
        '''message_to_doi process a source exist extracting doi retrieval
           records and saving them to doi table if dry_run is false.
           returns a count of doi found and error message is their is
           a problem'''
        n = 0 # Number of DOI processed from the message body
        err = ''
        err_cnt = 0
        if m.m_body:
            for i, line in enumerate(m.m_body.splitlines()):
                if line != '':
                    doi, url, err = extract_doi_and_url(line)
                    if err:
                        print(f'ERROR: msg {m.m_id} error found line {i}, {err}')
                        err_cnt += 1
                    if doi:
                        n += 1
                        d = Doi.get_or_none(doi = doi)
                        if d == None:
                            d = Doi()
                            d.doi = doi
                            d.created = datetime.now()
                        d.m_id = m.m_id
                        d.m_from = m.m_from
                        if url != None:
                            d.object_url = url
                        if err:
                            d.notes += f"ERROR: msg {m.m_id} error found line {i}, {err}\n"
                            d.status = 'processing_error' 
                        else:
                            d.status = 'unprocessed'
                        d.updated = datetime.now()
                        d.save()
        return n, err_cnt, err

    def get_unprocessed(self):
        return Doi.select().where(Doi.status == 'unprocessed')

    def get_metadata(self, doi, dry_run = False):
        if dry_run:
            print(f'Dry run, no data fetched with doi2eprintxml')
            return None, None
        #cmd = [ doi2eprintxml_cmd, '-mailto', doi2eprintxml_email, '-clsrules=true', doi ]
        cmd = [ doi2eprintxml_cmd, '-mailto', doi2eprintxml_email, '-json', '-clsrules=true', doi ]
        print(f'DEBUG get_metadata cmd:', cmd)
        return cmds.run(cmd)

def doi2eprintxml_version():
    cmd = [ 'doi2eprintxml', '-version' ]
    s, err = cmds.run(cmd)
    if err != None:
        if isinstance(err, bytes):
            err = err.decode('utf-8')
        return err.strip()
    if isinstance(s, bytes):
        s = s.decode('utf-8')
    return s.strip()

__doi2eprintxml_version__ = doi2eprintxml_version()


