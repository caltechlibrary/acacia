INSTALL ACACIA
==============

For installing ep3apid and doi2eprintxml see [EPrintools](https://github.com/caltechlibrary/eprinttools).

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
4. run Python 3's pip to install dependencies
5. Copy settings.ini-example to settings.ini
6. Edit settings.ini to conform to your installation
7. Generate the HTML pages per site configuration using the Makefile
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
./configure-database
make
```

If you are run a development version you can launch Acacia with

```
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

Consult your Apache 2 documentation for details on both. The Acacia application runs via Apache2 WSGI module. Restarting Apache2 if configured should restart Acacia.  The ep3apid service is run independently and normally installed such that you can start and stop the service via systemd (or launchctl on macOS). The ep3apid is used to manage access via Shibboleth ID lookup to Acacia.


EPrint Tools
------------

Acacia depends on EPrinttools already being installed.
You need version 1.1.1 or better of EPrinttools for authorization,
retrieving and processing data from CrossRef and DataCite. You can install
that by visiting [github.com/caltechlibrary/eprinttools/releases](https://github.com/caltechlibrary/eprinttools/releases) and downloading
and install the version of the tools suited to your computer.
The program `ep3apid` and `doi2epritxml` needs to be copied to the 
`bin` folder of Acacia.

Notes
-----

Setup virtual Python environment.

```
python3 -m venv venv
source venv/bin/activate
```

Clone idutils from https://github.com/ines-cruz/idutils

```
git clone git@github.com:ines-cruz/idutils
```

Then install via requirements.txt with pip.

