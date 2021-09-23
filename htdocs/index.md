---
title : Welcome to Acacia
---

Welcome to Acacia
=================

Acacia is a tool for converting DOI metadata into EPrint XML. The [DOI](https://doi.org) metadata is retrieved from [CrossRef](https://crossref.org) and [DataCite](https://datacite.org). Acacia supports collecting DOI via Email or through a simple data entry form.  The collected DOI can be used to look up metadata from CrossRef and DataCite resulting in EPrint XML suitable for importing into [CaltechAUTHORS](https://authors.library.caltech.edu).

Workflows
---------

- Email
    1. Get [Messages](./get-messages)
    2. Convert [Messages to DOI](./messages-to-doi)
    3. Review [Messages Report](./messages/)
- Data Entry
    1. [Add a DOI](add-doi)
- Retrieving metadata and generating EPrint XML
    1. Review the [DOI Report](./list/)
    2. For each DOI collected
        a. Review the link contents for DOI, URL of PDF
        b. If OK and you see the "look up" button, press it
        b. Click the Export link "EPrint XML" and save locally
        c. Download any related PDF for digital materials from either the DOI link or Object URL link (if one is provided)
        e. Open a browser window for [CaltechAUTHORS](https://authors.library.library.caltech.edu)
        f. Import the EPrint XML you downloaded
        g. Add the PDF, if you downloaded one, to the EPrints record
        h. Switch back to Acacia's [DOI Report](./list)
        i. In the row with DOI row in Acacia click the "remove" button to remove the DOI from the list



Reports
-------

- [Messages](./messages/)
- [DOI](./list/)

Misc
----

- [Help](./help/)
- [About Acacia](./about)
