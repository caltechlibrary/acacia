'''
remote.py provides an API for pull content either with Unix cli
or directly using Python web client.

Copyright
---------

Copyright (c) 2021 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

from . import cmds


def fetch_doi_metadata(doi):
    cmd = [ 'doi2eprintxml', doi ]
    return cmds.run(cmd)


