Developers -- Project Layout
=============================

This document provides a brief sketch of the Acacia package's layout.

acacia/cmds.py
--------------

The cmds object is used internally by Acacia for assemble commands run via the host operating system. The includes running the `doi2eprintxml` tool as well as using SSH to remotely access SQL content on the host EPrints server.

acacia/connections.py
---------------------

The connections object parses and structures DB connection data for use by SQLite3 and MySQL 8.  It allows the use of connection strings in the settings.ini file limiting the number of variables that need to be managed.

acacia/doi.py
-------------

The doi object models metadata related to retrieving objects from a DOI. This includes accessing the CrossRef/DataCite API via `doi2eprintxml` and accessing EPrints data via SSH scripts on the EPrints host

acacia/eprints.py
-----------------

This package models accessing EPrints metadata with either via SSH and hosted scripts or via MySQL DB connections.

acacia/messages.py
------------------

This models the email messages retrieved for processing.

acacia/persons.py
-----------------

This models the Acacia access by Library staff

acacia/settings.py
------------------

This contains a function that returns an example `settings.ini` file


<div class="paging">

Continue Reading
----------------

- [Up](developers.html "Developer documentation")
- [Next](people-manager.html "People Manager")
- [Prev](commands.html "Commands")

</div>
