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
from peewee import SqliteDatabase, Model, Field
from peewee import CharField, TextField, DateTimeField, BooleanField

from . import cmds

_db = SqliteDatabase(config('DATABASE', 'acacia.db'))

# e.g. 'Wed, 15 Jul 2020 12:13:29 -0700'
dt_email_format = '%a, %d %b %Y %H:%M:%S %z'

def setup_doi_table(db_name, table_name = 'doi'):
    '''setup a SQLite3 database table'''
    db = SqliteDatabase(db_name)
    if db.connect():
        if db.table_exists(table_name):
            print(f'''WARNING: {table_name} already exists in {db_name}''')
        else:
            db.create_tables([Doi])
            print(f'''{table_name} table created in {db_name}''')
    else:
        print(f'''ERROR: could not connect to {db_name}''')

def upgrade_doi_table(db_name, table_name = 'doi'):
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

workflow_states = [ 'unprocessed', 'processing_error', 'ready', 'edit', 'bundled', 'hold', 'completed', 'trash' ]

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
    status = Workflow(default = 'unprocessed')
    # bundle-name, this is a machine generated associated with a download
    bundle_name = CharField(default = '')
    # JSON of metadata retrieved from either CrossRef or DataCite
    # structure id based `doi2eprintxml -json DOI`, this can be
    # rendered as EPrintXML via `epfmt -xml < DOI.json > DOI.xml`
    metadata = TextField(default = '')
    # Any processing notes
    notes = TextField(default = '')
    # When was the record last updated
    updated = DateTimeField(default=datetime.now)
    # When the record was created
    created = DateTimeField(default=datetime.now)
    # EPrints eprint_id if known
    eprint_id = CharField(null = True, default = None)
    # EPrints repository id if known
    repo_id = CharField(null = True, default = None)

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
        is_url = False;
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
        cmd = [ 'doi2eprintxml', '-json', doi ]
        return cmds.run(cmd)


