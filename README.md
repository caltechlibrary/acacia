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

_Acacia_ is an internal Caltech Library project to find a _very_ lightweight solution for accepting publications into [CaltechAUTHORS](https://authors.library.caltech.edu) via a list of DOI. The basic idea is for ACM Open to email a list of DOI, one per line, to a known email address at Caltech Library where a bot then reads the email (via procmail or something similar), converts the DOIs into metadata, and harvests the article PDF for submission into the CaltechAUTHORS EPrints repository.

Installation
------------

Requirements

+ Python3
+ IMAP email account (and access credentials)
+ Emails with list of DOI, one per line
+ software in this repository setup to run periodically (e.g. via cron, systemd or launchd)

Details to be determined.

Usage
-----

Details to be determined.

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

Copyright (c) 2020, Caltech
All rights not granted herein are expressly reserved by Caltech.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


Authors and history
---------------------------

+ Mike Hucka
+ R. S. Doiel
+ Tommy Keswick
+ Tom Morrell

