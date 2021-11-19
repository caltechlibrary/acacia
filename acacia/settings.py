def settings_example():
   print('''
The "settings.ini" file should look something like

```
# ========================================================================
# @file    settings.ini
# @brief   Settings file for Acacia.
# @created 2021-03-19
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
# Path to the sqlite database, relative to here.
DATABASE_FILE = acacia.db

# BASE_URL this is the URL including path prefix which is used
# in linking the application together.
BASE_PREFIX = http://localhost:8080

# EP3API_URL is the URL to the ep3apid instance (e.g. http://localhost:8484)
EP3API_URL = http://localhost:8484
# REPO_ID the repository ID used by EP3API_URL.
REPO_ID = "REPO_ID"

# Email details. This is to access the mailbox of the submissions
# email account.

# Inbound IMAP Mailbox of submittions email address
# FIXME: You need to set these appropriate to your email provider
IMAP_HOST = imap.gmail.com
IMAP_SSL = true
IMAP_PORT   = 993

# Outbound IMAP if needed
# FIXME: You need to set these appropriate to your email provider
SMTP_HOST = smtp.gmail.com
SMTP_SSL = true
SMTP_REQUIRE_TLS = true
SMTP_AUTH = true
SMTP_SSL_PORT = 465
SMTP_TLS_PORT = 587

# Account info
# FIXME: You will need change the values for SUBMIT_EMAIL and PASSWORD
DISPLAY_NAME = "Author Submissions Bot"
SUBMIT_EMAIL = "CHANGE_ME_TO_THE_SUBMISSIONS_EMAIL_ADDRESS"
PASSWORD = "CHANGE_ME_TO_THE_SUBMISSIONS_EMAIL_PASSWORD"
```
''')
