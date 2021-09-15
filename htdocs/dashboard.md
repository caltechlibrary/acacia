---
title : Welcome to Acacia
---

Welcome to ACACIA
=================

Acaca is a micro webservice for managing CaltechAUTHORS submissions
via DOI.

Workflows
---------

Two workflows are provided depending on where the DOI(s) originate
before getting into processing the DOI(s).

- EMail
    1. [Get Messages](get-messages)
    2. [Messages to DOI](messages-to-doi)
    3. [Review message list](messages/)
- Data Entry
    1. [Add a DOI](add-doi)

This is followed by actually processing the DOI(s) by retrieving
metadata from CrossRef/DataCite and then using the generated EPrint XML
for importing into [CaltechAUTHORS](https://authors.library.caltech.edu).

- Processing submitted DOI
    1. [Retrieve Metadata](retrieve-metadata)
    2. [Review DOI list](list/)
    3. For each DOI record in the list
        a. Review the DOI, Object URL and any existing EPrints record
        b. If no-EPrints record exists click the Export link "EPrint XML"
           and save locally
        c. Download any related PDF for digital materials from either the DOI link or Object URL link (if one is provided)
        d. Import the EPrint XML and PDF into [CaltechAUTHORS](https://authors.library.library.caltech.edu)
        e. Confirm EPrints import was successful
        f. In the DOI row in Acacia click the "remove" button to remove the row from the list


Reports
-------

- [Messages](messages/)
- [DOI List](list/)

Misc
----

- [Help](help/)
    - [Overview](help/overview.html)
- [About Acacia](about)
