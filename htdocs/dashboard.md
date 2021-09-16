---
title : Welcome to Acacia
---

Welcome to ACACIA
=================

Acaca is a micro webservice for managing [CaltechAUTHORS](https://authors.library.caltech.edu) submissions via DOI retrieving metadata from [CrossRef](https://crossref.org) and [DataCite](https://datacite.org). Acacia supports retrieving data by providing one or more DOI via EMail or through a simple data entry form.  The collected DOI can be used to retrieve metadata from CrossRef and DataCite resulting in EPrint XML suitable for importting into CaltechAUATHORS.

Workflows
---------

- EMail
    1. [Get Messages](get-messages)
    2. [Messages to DOI](messages-to-doi)
    3. [Review message list](messages/)
- Data Entry
    1. [Add a DOI](add-doi)
- Retrieving metadata and generating EPrints XML
    1. [Review DOI list](list/) the generated from the EMail or data entry
    2. For each DOI record in the list
        a. Review the DOI, PDF URL, press the "Lookup" button if needed
        b. Click the Export link "EPrint XML" and save locally
        c. Download any related PDF for digital materials from either the DOI link or Object URL link (if one is provided)
        e. Import the EPrint XML and PDF into [CaltechAUTHORS](https://authors.library.library.caltech.edu)
        f. Confirm EPrints import was successful
        g. In the DOI row in Acacia click the "remove" button to remove the row from the list


Reports
-------

- [Messages](messages/)
- [DOI List](list/)

Misc
----

- [Help](help/)
    - [Overview](help/overview.html)
- [About Acacia](about)
