Acacia<img width="18%" align="right" src=".graphics/acacia-icon.svg">
=======================================================================

Acacia ("_**A**utomated **C**altech**A**UTHORS **C**atalog **I**ngest **A**gent_") is a project to facilitate [ACM Open](https://libraries.acm.org/subscriptions-access/acmopen)'s direct submissions into [CaltechAUTHORS](https://authors.library.caltech.edu) using a simple mail-based workflow.


Table of contents
-----------------

* [Introduction](#introduction)
* [Installation](#installation)
* [Usage](#usage)
* [Known issues and limitations](#known-issues-and-limitations)
* [Getting help](#getting-help)
* [Contributing](#contributing)
* [License](#license)
* [Authors and history](#authors-and-history)


Introduction
------------

_Acacia_ is an internal Caltech Library project to find a _very_ lightweight solution for accepting publications into [CaltechAUTHORS](https://authors.library.caltech.edu) via a list of DOI. The basic idea started as a way for ACM Open to email a list of DOI, one per line, to a known email address at Caltech Library where a bot then reads the email (via procmail or something similar), converts the DOIs into metadata, and harvests the article PDF for submission into the CaltechAUTHORS EPrints repository. We believe this approach can be applied more broadly to other types of submissions.


Installation
------------

Requirements

+ [EPrint Tools >= 1.1.1](https://github.com/caltechlibrary/eprinttools/releases)
    - [doi2eprintxml](https://caltechlibrary.github.io/eprinttools/docs/doi2eprintxml)'s to retrieve the metadata associated with a DOI from CrossRef or DataCite (version 1.1.0 or better)
    - [ep3apid](https://caltechlibrary.github.io/eprinttools/docs/ep3apid) / to handling importing records and quering the EPrints repository for records and user accounts.
+ Python3
+ MySQL (used by EPrints)
+ IMAP email account (and access credentials)
+ Emails with list of DOI, one per line
+ software in this repository setup to run periodically (e.g. via cron, systemd or launchd)

See [INSTALL.md](INSTALL.md) for full details.


Usage
-----

The application consist of several parts. 

1. A Bottle based Python3 application for UI
2. EPrinttools' ep3apid for interacting with our EPrints repository
3. EPrinttools' doi2eprintxml for retrieving metadata from CrossRef or DataCite services

Both the Bottle application and ep3apid need to run as services on your server. In addition the Bottle application is expected to run behind Shibboleth and Apache2. The Bottle application functions as the interaction point querying the ep3apid service as needed as well as calling doi2eprintxml as needed.  

After setting up Apache2 and Shibboleth the Bottle application runs as a WSGI service via Apache2. The Bottle application uses a settings.ini file to know where to access the ep3apid service as well as some additional configuration.   For the Bottle application to function it needs to have ep3apid running on localhost. This service has it's own configuration in a "settings.json" file. See [EPrinttools](https://github.com/caltechlibrary/eprinttools) for details on setting it up and configuring it.

To install this application review [INSTALLmd](INSTALL.html). Download both [Acacia](https://github.com/caltechlibrary/Acacia/releases) and [EPrinttools](https://github.com/caltechlibrary/eprinttools/releases). Unzip the respective files and copy into the desired locations on your system (e.g. /Sites/acacia for the Bottle app and /usr/local/bin for EPrinttools).  Edit the settings.ini appropriately for Acacia and the settings.json for EPrinttools. Configure Apache2 for Shibboleth and WSGI for Acacia. Restart Apache2.  Start the ep3apid service using your updated `settings.json` file.  The ep3apid daemon can be configured to run via systemd or macOS's launchd.



Known issues and limitations
----------------------------

This is a proof of concept to facilitate ACM Open's submissions
to CaltechAUTHORS using a very light weight approach. Requires
email accounts to be setup and exchanged, as well as credentials
to access the service email account.

Getting help
------------

Use the GitHub issue tracker for this project to obtain help.

https://github.com/caltechlibrary/acacia/issues


Contributing
------------

This is an internal project for Caltech Library. It is mainly of
public interest as a reference to implementing a similar solution
for submissions from publishers.  If you'd like to participate
submit an request via the issue tracker.

License
-------

Copyright (c) 2021, Caltech
All rights not granted herein are expressly reserved by Caltech.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


Authors and history
-------------------

+ R. S. Doiel
+ Mike Hucka
+ Tommy Keswick
+ Tom Morrell
+ George Porter

