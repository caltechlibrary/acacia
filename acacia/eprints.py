#!/usr/bin/env python3

#
# eprints.py is responsible interfacing with EPrints for CaltechAUTHORS
# repository. It relies on a database connection to the MySQL host
# that backs CaltechAUTHORS.
#
import os
import sys

import mysql.connector
from mysql.connector import errorcode

from .connections import ConnectionInfo


class EPrintsDB:
    _cnx = None
    
    def __init__(self, connection_string = None):
        if connection_string == None:
            raise ValueError('Missing connection string')
            return
        _con = ConnectionInfo()
        _con.parse(connection_string)
        con = _con.toDict()
        if con == None:
            raise ValueError(f'Could not parse "{connection_string}"')
            return
        try:
            self._cnx = mysql.connector.connect(**con)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            return

    def __del__(self):
        if self._cnx != None:
            self._cnx.close()
    
    def get_eprint_id_by_doi(self, doi):
        # Get a cursor
        cursor = self._cnx.cursor()
        # SQL for returning eprint id from eprint
        query = f'''SELECT eprintid FROM eprint WHERE doi = %s LIMIT 1'''
        cursor.execute(query, (doi))
        eprint_id = cursor.eprintid
        cursor.close()
        return eprint_id

