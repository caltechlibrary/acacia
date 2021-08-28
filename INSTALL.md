INSTALL ACACIA
==============

Acacia is an experimental Python web application.  There is no installer
currently implemented. The general recipe is

1. Download and install [eprinttools](https://github.com/caltechlibrary/eprinttools/releases) per eprinttools [instructions](https://github.com/caltechlibrary/eprinttools/blob/main/INSTALL.md)
2. Clone the Acacia git [repository](https://github.com/caltechlibrary/acacia) to your machine
3. Change into the repostiory directory on your machine
4. run Python 3's pip to install dependencies
5. Configure the Acacia database
6. Setup user accounts.
7. Setup/run the web service

This is an example shell session of taking the following step 2 through
8 in a development environment.  NOTE: It assume's eprinttools already
has been installed.

```bash
git clone git@github.com:caltechlibrary/acacia
cd acacia
python3 -m pip install -r requirements.txt
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

Concult your Apache 2 documentation for details on both.

In a production like environment you need to setup several cron jobs
to run the automated processes

1. __get-messages__ retrieves email from the authors.submission@library.caltech.edu email account
2. __messages-to-doi__ processes the retrieved messages and parses out any DOI and object links found in the messages
3. __retrieve-metadata__ retrieves information from CrossRef and DataCite via the __doi2eprintxml__ tool
 
Normally these processes would be run in this order. Probably run them about every 15 to 30 minutes during business hours.  It is also possible to trigger these script on demand. That's something that should be explored in the pilot use of this experimental application.

EPrint Tools
------------

Acacia depends on EPrinttools already being installed.
You need version 1.0.1 or better of EPrint Tools for retrieving
and processing data from CrossRef and DataCite. You can install
that by visiting [github.com/caltechlibrary/eprinttools/releases](https://github.com/caltechlibrary/eprinttools/releases) and downloading
and install the verison of the tools suited to your computer.
The program `doi2epritxml` needs to be copied to the `bin` folder
of Acacia.


