INSTALL ACACIA
==============

Requirements
------------

- GNU Make
- Pandoc (used in generating the static HTML pages and some templates)
- MkPage (used in generating the static HTML pages and some templates)
- Python3 and the modules in requirements.txt

Installation Steps
------------------

Acacia is an experimental Python web application.  There is no installer
currently implemented. The general recipe is

1. Download and install [eprinttools](https://github.com/caltechlibrary/eprinttools/releases) per eprinttools [instructions](https://github.com/caltechlibrary/eprinttools/blob/main/INSTALL.md)
2. Clone the Acacia git [repository](https://github.com/caltechlibrary/acacia) to your machine
3. Change into the repository directory on your machine
4. Copy settings.ini-example to settings.ini
5. Edit settings.ini to conform to your installation
6. Generate the HTML pages per site configuration
7. run Python 3's pip to install dependencies
8. Configure the Acacia database
9. Setup user accounts.
10. Setup/run the web service

This is an example shell session of taking the following step 2 through
8 in a development environment.  NOTE: It assumes eprinttools already
has been installed.

```bash
git clone git@github.com:caltechlibrary/acacia
cd acacia
python3 -m pip install -r requirements.txt
cp settings.ini-example settings.ini
vi settings.ini
make
./configure-database
./people-manager add 
    uname=$USER \
    display_name="Test user" \
    email="test@example.edu" \
    role=library
./run-server -m debug -u $USER
```


Production-like setup
---------------------

Acacia is experimental software. It cannot be stressed enough that it
is not ready for prime time. That said it is useful to have potential
users of the application try it out. As a result you need to setup a
production like environment to provide the experience of how it would
work if you were in production.

For this to work you need to configure Apache 2 to support both WSGI
python programs and authentication. In a production system Authentication
should be some single sign on system like Shibboleth. But in showing
potential system users the application you could just use Apache Basic Auth
behind SSL.

Consult your Apache 2 documentation for details on both.

In a production like environment you need to setup several cron jobs
to run the automated processes

1. __get-messages__ retrieves email from the authors.submission@library.caltech.edu email account
2. __messages-to-doi__ processes the retrieved messages and parses out any DOI and object links found in the messages
3. __retrieve-metadata__ retrieves information from CrossRef and DataCite via the __doi2eprintxml__ tool
 
Normally these processes would be run in this order. Probably run them about every 15 to 30 minutes during business hours.  It is also possible to trigger these script on demand. That's something that should be explored in the pilot use of this experimental application.

You can run these scripts via cron to run nightly. Note the retrieve-metadata script can cause the web application to be briefly unavailable when it causing Apache to return a 500 error. This is probably a result of the time that the SQlite3 database is locked and unreadable by Apache's WSGI service.

```bash
    #!/bin/bash
    
    #
    # Workflow processes requests that come in via the submit email account
    # as well as those DOI added manually. 
    #
    # 1. Get emails messages
    # 2. Convert email messages to doi
    # 3. Retrieve metadata for each doi
    #
    export PATH="/bin:/usr/bin:/usr/local/bin"
    cd /Sites/acacia
    if [ "$1" = "full" ]; then
    ./get-messages
    ./messages-to-doi
    fi
    ./retrieve-metadata
```

EPrint Tools
------------

Acacia depends on EPrinttools already being installed.
You need version 1.0.1 or better of EPrint Tools for retrieving
and processing data from CrossRef and DataCite. You can install
that by visiting [github.com/caltechlibrary/eprinttools/releases](https://github.com/caltechlibrary/eprinttools/releases) and downloading
and install the version of the tools suited to your computer.
The program `doi2epritxml` needs to be copied to the `bin` folder
of Acacia.


