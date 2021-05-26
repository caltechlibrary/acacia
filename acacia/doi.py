#!/usr/bin/env python3

#
# doi.py is responsible for converting a stored (email) message
# include a series of retrival records (one per doi).  DOI retrieval
# records can then be aggregated to generate EPrintXML as well as a
# list of PDF urls to retrieve before importing into EPrints.
#
import os
import sys
from datetime import datetime

from decouple import config
from peewee import SqliteDatabase, Model, Field
from peewee import CharField, TextField, DateTimeField, BooleanField

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

def populate_field(key, msg, default = ''):
    field = None
    if key in msg:
        field = msg[key]
    else:
        field = default
    return field

workflow_states = [ 'unprocessed', 'processed', 'hold', 'completed' ]

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
    object_url = CharField()
    # Workflow status
    status = Workflow()
    # Submitted By: The From/Reply To value for submissions via email address, otherwise uname via SSO record creation
    submitted_by = CharField() 
    # If submitted by EMail record the message id from the message table
    email_msg_id = CharField()
    # Any processing notes
    notes = TextField()
    # Who updated the record last
    updated_by = CharField()
    # When was the record last updated
    updated = DateTimeField()

    class Meta():
        database = _db

def unquote(s):
    s = s.strip()
    if s.startswith("'"):
        return s.strip("'")
    elif s.startswith('"'):
        return s.strip('"')
    return s.strip()

