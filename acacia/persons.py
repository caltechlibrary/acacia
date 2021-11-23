'''
people.py provides account profiles for a persons based on contents of
the user table in your EPrints repository as accessed from the ep3apid
service.

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

## from . import cmds
from .ep3apid import Ep3API

import os

## Figure out how are authentication and authorization is configured.
#_db = SqliteDatabase(config('DATABASE_FILE', default='acacia.db'))

repo_id = config('REPO_ID', 'caltechauthors')
ep3apid_url = config('EP3APID_URL', 'http://localhost:8484')
ep3api = Ep3API(ep3apid_url, repo_id)

if not ('environ' in globals()):
    environ = {'REMOTE_USER': None}


# GuestPerson only exists while REMOTE_USER available in the environment.
# It is not stored in the person table as the Person model is.
class GuestPerson:
    '''GuestPerson is an object for non-staff people.  It has the same
    signature but is not persisted in the person table of the database.
    '''
    def get_or_none(self, uname):
        return None

    def has_role(self, required_role):
        return False

class Person:
    def __init__(self, uname):
        self.userid = 0
        self.uname = ''
        self.role = ''
        self.display_name = ''
        self.updated = ''
        self.get_or_none(uname)

    def get_or_none(self, uname):
        u, err = ep3api.user(uname)
        if not err:
            if 'userid' in u:
                self.userid = u['userid']
            if 'username' in u:
                self.uname = u['username']
            if 'type' in u:
                self.role = u['type']
            if 'name' in u:
                name = u['name']
            if 'family' in name and 'given' in name:
                self.display_name = f'{name["family"]}, {name["given"]}'
            self.updated = u["joined"]
            return self 
        return None

    def has_role(self, required_role):
        return self.role == required_role

def person_from_environ(environ):
    if 'REMOTE_USER' in environ:
        # NOTE: If we're shibbed then we always return a Person object.
        # Either they are a known person (e.g. library staff) or other community
        # member without a role.
        person = Person(environ['REMOTE_USER'])
    else:
        person = Person()
    return person

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
    
    def list_people(self, kv = None):
        '''list people in the Repository usering username'''
        if not kv:
            print(f'''User Id\tUsername\tName\tRole\tUpdated''')
            usernames, err = ep3api.usernames()
            person = Person(None)
            for uname in usernames:
                u = person.get_or_none(uname)
                if u != None:
                    print(f'''{u.userid}\t{u.uname}\t{u.display_name}\t{u.role}\t{u.updated}''')
        elif isinstance(kv, dict) and 'uname' in kv:
            u = Person(kv['uname'])
            print(f'''
        User Id:  {u.userid}
        Username: {u.uname}
            Name: {u.display_name}
            Role: {u.role}
         Updated: {u.updated}
    ''')
