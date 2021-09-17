Commands
========

The following are commands that can be run from the command
line of the project's root directory. These should not be run
while the Web UI is operating as they can cause Apache to return
a 500 HTTP error if the databases is not available.

1. configure-database will create a SQLite3 databases needed to run Acacia
2. get-messages will querry an IMAP to retrieve emails containing submitted DOI
3. message-to-doi will convert the messages, extract a list of DOI and add those to the list of DOI to be processed
4. retrieve-meatadata will take the list of unprocessed DOI retrieve metadata via CrossRef and DataCite as well as query EPrints for existing records with given DOI
5. people-manager is a command line tool for adding/removing or updating a person' access to Acacia via username and role assignment

Test commands
-------------

1. test-eprints-ssh is a test of accessing EPrints via SSH using a prefined setup of scripts forming an API


<div class="paging">

Continue Reading
----------------

- [Up](developers.html "Developer documentation")
- [Next](package-layout.html "Project layout")
- [Prev](requirements.html "Requirements")

</div>
