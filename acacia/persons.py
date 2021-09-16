'''
people.py provides account profiles for a persons based on their fields
in the person table in an SQLite3 database.

It does not provide suppport for authentication, that needs to be
provided by your front end web server such as Apache 2. If you
have Apache2's Basic Auth the PersonManager class will attempt
to store/update/remove passwords (aka secrets) via the
Apache htpasswd program. 

No password are stored in the SQLite3 person table.

Copyright
---------

Copyright (c) 2021 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

import os
import sys
import shutil
from datetime import datetime
from subprocess import Popen, PIPE

from getpass import getpass

from decouple import config
from peewee import SqliteDatabase, Model
from peewee import AutoField, CharField, TimestampField

from . import cmds

import os

# Figure out how are authentication and authorization is configured.
_db = SqliteDatabase(config('DATABASE_FILE', default='acacia.db'))

def setup_person_table(db_name, table_name = 'person'):
    '''setup a SQLite3 database table'''
    db = SqliteDatabase(db_name)
    if db.connect():
        if db.table_exists(table_name):
            print(f'''WARNING: {table_name} already exists in {db_name}''')
        else:
            db.create_tables([Person])
            print(f'''{table_name} table create in {db_name}''')
    else:
        print(f'''ERROR: could not connect to {db_name}''')
        
def upgrade_person_table(db_name, table_name = 'person'):
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
    

# Person is for development, it uses a SQLite3 DB to user
# connection validation data.
class Person(Model):
    uname = CharField()  # user name, e.g. janedoe
    role = CharField()   # role is usually empty or "library"
    display_name = CharField() # display_name, optional
    email = CharField() # The email address to use for DOI form submission
    updated = TimestampField() # last successful login timestamp

    def has_role(self, required_role):
        return self.role == required_role

    class Meta:
        database = _db


# GuestPerson only exists while REMOTE_USER available in the environment.
# It is not stored in the person table as the Person model is.
class GuestPerson():
    '''GuestPerson is an object for non-staff people.  It has the same
    signature but is not persisted in the person table of the database.
    '''
    def __init__(self, uname = '', display_name = '', role = '', email = ''):
        self.uname = uname               # user name, e.g. janedoe (or Shib ID)
        self.display_name = display_name # display_name, optional
        self.role = role                 # role is empty or "staff"
        self.email = email               # email, maybe different from Shib ID
        self.updated = datetime.now()

    def has_role(self, required_role):
        return self.role == required_role


def person_from_environ(environ):
    if 'REMOTE_USER' in environ:
        # NOTE: If we're shibbed then we always return a Person object.
        # Either they are a known person (e.g. library staff) or other community
        # member without a role.
        person = Person.get_or_none(Person.uname == environ['REMOTE_USER'])
        if person == None:
            person = GuestPerson()
            person.uname = environ['REMOTE_USER']
            person.display_name = environ['REMOTE_USER']
        return person
    else:
        return None

def normalize_str(s):
    if isinstance(s, bytes):
        return s.decode('utf-8')
    return s

#
# NOTE: The following are used by people-manager and are not expected
# to be used in the web UI.
#
class PersonManager:
    '''PersonManager provides a class to build a CLI person manager'''
    def __init__(self, db_name, htpasswd = None, password_file = None):
        self.htpasswd = htpasswd
        self.password_file = password_file
        self.db_name = db_name
        
    def _update_htpasswd(self, uname, secret):
        '''Update the password for user using htpasswd from Apache'''
        if (self.htpasswd == None) or (self.password_file == None):
            print(f'ERROR: not setup for Apache htpasswd support')
            sys.exit(1)
        if not os.path.exists(self.password_file):
            print(f'ERROR: password file {self.password_file} does not exist')
            sys.exit(1)
        if not secret:
            secret = getpass(prompt='Password: ', stream = None)
        if not secret:
            return False
        cmd = [ self.htpasswd, '-b', self.password_file, uname, secret ]
        with Popen(cmd, stdout = PIPE, stderr = PIPE) as proc:
            out = normalize_str(proc.stdout.read())
            err = normalize_str(proc.stderr.read())
            if out:
                print(out)
            if err:
                print(err)
        return True 
    
    def _delete_htpasswd(self, uname):
        if (self.htpasswd == None) or (self.password_file == None):
            print(f'ERROR: not setup for Apache htpasswd support')
            sys.exit(1)
        if not os.path.exists(self.password_file):
            print(f'ERROR: password file {self.password_file} does not exist')
            sys.exit(1)
        cmd = [ self.htpasswd, '-D', self.password_file, uname ]
        with Popen(cmd, stdout = PIPE, stderr = PIPE) as proc:
            out = normalize_str(proc.stdout.read())
            err = normalize_str(proc.stderr.read())
            if out:
                print(out)
            if err:
                print(err)
        return True 
    
    def list_people(self, kv):
        '''list people in the SQLite3 database table called person'''
        if 'uname' in kv:
            row = (Person.select().where(Person.uname == kv['uname']).get())
            if row == None:
                print(f'''Cannot find person {kv["uname"]}''')
            else:
                print(f'''
        Username: {row.uname}
            Name: {row.display_name} <{row.email}>
            Role: {row.role}
         Updated: {row.updated}
    ''')
        else:
            print(f'''Username\tName\tRole\tUpdated''')
            query = (Person.select().order_by(Person.display_name))
            for row in query:
                print(f'''{row.uname}\t{row.display_name} <{row.email}>\t{row.role}\t{row.updated}''')
    
    def add_people(self, kv):
        if not 'uname' in kv:
            print(f'''ERROR: uname is required''')
            sys.exit(1)
        if ('secret' in kv):
            if self.htpasswd != None:
                self._update_htpasswd(kv['uname'], kv['secret'])
            else:
                print(f'WARNING: secrets not supported')
        for key in [ 'role', 'display_name', 'email' ]:
            if not key in kv:
                kv[key] = ''
        if not 'display_name' in kv:
            kv['display_name'] = uname
        user = Person(uname = kv['uname'], role = kv['role'], display_name = kv['display_name'], email = kv['email'])
        user.save()
    
    def update_people(self, kv):
        user = Person.select().where(Person.uname == kv['uname']).get()
        if user == None:
            print(f'ERROR {kv["uname"]} does not exist')
            sys.exit(1)
        if ('secret' in kv):
            if self.htpasswd != None:
                self._update_htpasswd(user.uname, kv['secret'])
            else:
                print(f'WARNING: secrets not supported')
        if 'display_name' in kv:
            user.display_name = kv['display_name']
        if 'role' in kv:
            user.role = kv['role']
        user.save()
    
    def remove_people(self, kv):
        if not 'uname' in kv:
            print(f'''WARNING: uname is required''')
            sys.exit(1)
        nrows = Person.delete().where(Person.uname == kv['uname']).execute()
        if self.htpasswd != None:
            self._delete_htpasswd(kv['uname'])
        print(f'''{nrows} row deleted from person in {self.db_name}''')
    
