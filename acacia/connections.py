#!/usr/bin/env python3

#
# connections.py is responsible for converting a connection string
# in URI form to component parts for MySQL or SQLite3 databases.
#
import os
from urllib.parse import urlparse

class ConnectionInfo:
    '''ConnectionInfo provides a means to parse a URI containing a
       DB connection and split it into a components.
       Examples:
           
         con_info = ConnectionInfo()

         # Parse a MySQL connection string
         if con_info.parse("mysql://USER:PASSWD@example.edu/DB_NAME"):
             print(f'host: {con_info.host}:{con_info:port}')
             print(f'DB Name: {con_info.name}')
         else:
             print("Can't parse URL for DB connect')

         # Parse an SQLite3 connection string
         if con_info.parse("sqlite3://PATH_TO_DB/DB_NAME"):
             print(f'host (None:None): {con_info.host}:{con_info:port}')
             print(f'DB Name (Path to Sqlite3 DB): {con_info.name}')
         else:
             print("Can't parse URL for DB connect')

    '''
    db_type = None
    host = None
    port = None
    name = None
    user = None
    password = None

    def __init__(self, host = None, port = None, name = None, user = None, password = None):
        self.host, self.port, self.name = host, port, name
        self.user, self.password = user, password

    def parse(self, uri):
        u = urlparse(uri)
        if u.scheme == 'sqlite3':
            self.db_type = 'sqlite3'
            self.host, self.port, self.name = None, None, None
            self.user, self.password = None, None
            if u.host and u.path:
                self.name = os.path.join(u.host, u.path)
            elif u.path:
                self.name = u.path
            else:
                return False
        if u.scheme == 'mysql':
            self.db_type = u.scheme
            self.name, self.user, self.password = '', '', ''
            if u.hostname:
                self.host = u.hostname
            else:
                self.host = 'localhost'
            if u.port:
                self.port = u.port
            else:
                self.port = '3306'
            if len(u.path) > 1:
                self.name = u.path[1:]
            if u.username:
                self.user = u.username
            if u.password:
                self.password = u.password

    def toDict(self):
        if self.db_type == 'mysql':
            return { 'user': self.user, 'password': self.password,
                     'host': self.host, 'port': self.port,
                     'database': self.name, 'raise_on_warnings': True }
        elif self.db_type == 'sqlite3':
            return { 'db': self.name }
        else:
            return None

