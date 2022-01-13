'''
Caltech Acacia (Digital Borrowing System), an implementation of controlled
digital lending by the Caltech Library.

Copyright
---------

Copyright (c) 2021 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

# Package metadata ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# This is set of variables is to identify the Python software package.  These
# values are _not_ presented in the user interface of Acacia, except for the
# version number.  The information presented to Acacia users, like the contact
# email address, are set elsewhere, not here.
#
#  ╭────────────────────── Notice ── Notice ── Notice ─────────────────────╮
#  |    The following values are automatically updated at every release    |
#  |    by the Makefile. Manual changes to these values will be lost.      |
#  ╰────────────────────── Notice ── Notice ── Notice ─────────────────────╯

__app__         = 'Acacia'
__version__     = '0.0.7'
__description__ = 'A content submission system for CaltechAUTHORS using DOI metadata retrieval.'
__url__         = 'https://github.com/caltechlibrary/acacia'
__author__      = 'Robert S. Doiel, Michael Hucka, Thomas E Morrell, Tommy Keswick, George Porter'
__email__       = 'helpdesk@library.caltech.edu'
__license__     = 'BSD 3-clause'


# Exports.
# .............................................................................

from .routes import acacia
from .ep3apid.ep3api import Ep3API
from .ep3apid.user import User


# Miscellaneous utilities.
# .............................................................................

def print_version():
    print(f'{__name__} version {__version__}')
    print(f'Authors: {__author__}')
    print(f'URL: {__url__}')
    print(f'License: {__license__}')
