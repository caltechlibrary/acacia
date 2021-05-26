# ==========================================================================
# @file    configure-sqlite3.py
# @brief   Setup the SQLite3 database for acacia
# @created 2021-05-26
# @license Please see the file named LICENSE in the project directory
# @website https://github.com/caltechlibrary/dibs
# ==========================================================================

from datetime import datetime, timedelta
from decouple import config
from peewee import SqliteDatabase

from acacia.email import Message
from acacia.people import Person

db = SqliteDatabase(config('DATABASE_FILE', default='acacia.db'))

# Peewee autoconnects to the database if doing queries but not other ops.
db.connect()
db.create_tables([Message, Person])

print('-'*50)
print('Now use people-manager to add users')
print('-'*50)
