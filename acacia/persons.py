'''
people.py provides account profiles for a persons based on contents of
the user table in your EPrints repository as accessed from the ep3apid
service.

It does not provide suppport for authentication, that needs to be
provided by your front end web server such as Apache 2 or Apache 2
and Shibboleth.

No password are stored by the Acacia application.

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


## from . import cmds
from .ep3apid import Ep3API, User

repo_id = config('REPO_ID', 'caltechauthors')
ep3apid_url = config('EP3APID_URL', 'http://localhost:8484')
api = Ep3API(ep3apid_url, repo_id)

# GuestPerson only exists while REMOTE_USER available in the environment.
# It is not stored in the person table as the Person model is.
class GuestPerson(User):
    '''GuestPerson is an object for non-staff people.  It has the same
    signature but is not persisted in the person table of the database.
    '''
    def get_or_none(self, uname):
        return None

class Person(User):
    def __init__(self, uname = None):
        '''Person inits with a username rather than a dict'''
        if isinstance(uname, str):
            m, err = api.user(uname)
            if not err:
                User.__init__(self, m)
            else:
                User.__init___(self)
        else:
            User.__init__(self)

    def get_or_none(self, uname):
        m, err = api.user(uname)
        self.from_dict(m)
        return m

def person_from_environ(environ):
    if 'REMOTE_USER' in environ:
        remote_user = environ['REMOTE_USER']
        if '@' in remote_user:
            uname, host = remote_user.split('@', 2)
        else:
            uname = remote_user
        # NOTE: If we're shibbed use the REMOTE_USER value to 
        # retrieve person from EPrint user table without the @caltech.edu
        return Person(uname)
    return Person()

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
            print(f'''User Id\tUsername\tName\tRole\tCreated''')
            usernames, err = api.usernames()
            person = Person(None)
            required = [ 'admin', 'editor' ]
            for uname in usernames:
                u = Person(uname)
                if u != None and u.has_role(required):
                    print(f'''{u.userid}\t{u.uname}\t{u.display_name}\t{u.role}\t{u.created}''')
        elif isinstance(kv, dict) and 'uname' in kv:
            u = Person(kv['uname'])
            print(f'''
        User Id:  {u.userid}
        Username: {u.uname}
            Name: {u.display_name}
            Role: {u.role}
         Updated: {u.updated}
    ''')
