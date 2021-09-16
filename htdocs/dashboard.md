---
title : Welcome to Acacia
---

Welcome to ACACIA
=================

Acaca generates EPrints XML based on the [DOI](https://doi.org) and the metadata from [CrossRef](https://crossref.org) and [DataCite](https://datacite.org). Acacia supports retrieving data by providing one or more DOI via EMail or through a simple data entry form.  The collected DOI can be used to look up metadata from CrossRef and DataCite resulting in EPrint XML suitable for importting into [CaltechAUATHORS](https://authors.library.caltech.edu).

Workflows
---------

- EMail
    1. [Get Messages](get-messages)
    2. [Convert Messages to DOI](messages-to-doi)
    3. [Review message list](messages/)
- Data Entry
    1. [Add a DOI](add-doi)
- Retrieving metadata and generating EPrints XML
    1. [Review the collected DOI](list/)
    2. For each DOI collected
        a. Review the link contents for DOI, URL of PDF
        b. If OK and you see the "look up" button, press it
        b. Click the Export link "EPrint XML" and save locally
        c. Download any related PDF for digital materials from either the DOI link or Object URL link (if one is provided)
        e. Open a browser window for [CaltechAUTHORS](https://authors.library.library.caltech.edu)
        f. Import the EPrint XML you downloaded
        g. Add the PDF, if you downloaded one, to the EPrints record
        h. Switch back to Acacia's [DOI list](./list)
        i. In the row with DOI row in Acacia click the "remove" button to remove the DOI from the list



Reports
-------

- [Messages](messages/)
- [DOI List](list/)

Misc
----

- [Help](help/)
    - [Overview](help/overview.html)
- [About Acacia](about)
