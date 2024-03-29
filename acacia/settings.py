def settings_example():
   print('''
# ========================================================================
# @file    settings.ini
# @brief   Settings file for Acacia.
# @created 2021-11-24
# @license Please see the file named LICENSE in the project directory
# @website https://github.com/caltechlibrary/acacia
# 
#     ,------------------- Notice -- Notice -- Notice -------------------.
#     | This file must be located in the same directory as               |
#     | process_mail.py.                                                 |
#     `------------------------------------------------------------------'
#
# ========================================================================

[settings]

# The MySQL data base connection information
DATABASE_NAME = acacia
DATABASE_HOST = localhost:3306
#FIXME: change this DATABASE_USER and DATABASE_PASSWORD
# to match your database configuration.
DATABASE_USER = acacia 
DATABASE_PASSWORD = CHANGE_ME_SOME_SECRET_THING_HERE

# Base url for Acacia Application
# NOTE: This is needed in part to render the static content for via mkpage
# and Pandoc
BASE_URL = http://localhost:8080

# EPRINT_URL is the URL embedded in EPrints XML
#FIXME: Set this to your eprints repository URL
EPRINT_URL = https://eprints.example.edu


# The URL to prefix to view the record. E.g.
#     https://authors.library.caltech.edu ...
#     ... /cgi/users/home?screen=EPrint::View&eprintid=
VIEW_URL = https://eprints.example.edu/cgi/users/home?screen=EPrint::View&eprintid=

# EP3APID_URL the URL to the eprinttools' ep3apid service
EP3APID_URL = http://localhost:8484
# The repo_id used by the ep3apid service.
REPO_ID = caltechauthors


# Email details. This is to access the mailbox of the submissions
# email account.

# Inbound IMAP Mailbox of submittions email address
# NOTE: Codebase assumes SSL support
# FIXME: you need to set these appropriate to your email provider
IMAP_HOST = imap.gmail.com
IMAP_PORT   = 993

# Outbound IMAP if needed
# NOTE: Codebase assumes SSL/TLS support
# FIXME: you need to set these appropriate to your email provider
SMTP_HOST = smtp.gmail.com
SMTP_SSL_PORT = 465
SMTP_TLS_PORT = 587

# Account info
#FIXME: you need to EMAIL and SECRET appropriately
DISPLAY_NAME = 'Author submission bot'
SUBMIT_EMAIL = 'CHANGE_ME_TO_THE_SUBMISSIONS_EMAIL_ADDRESS'
SECRET = 'CHANGE_ME_TO_THE_SUBMISSIONS_EMAIL_PASSWORD'


# Location of the doi2eprintxml command line program.
# NOTE: if this is not in your path you need to specify the 
# full path to the program.
DOI2EPRINTXML = doi2eprintxml

# The following run mode options are recognized:
#   "normal":  use adapter.wsgi without special options
#   "verbose": use adapter.wsgi with verbose logging options
# When started using the program run-server included with DIBS, this value
# maybe overriden by command-line options given to run-server.
RUN_MODE = verbose

''')
