Help -- Available Reports
=========================

Two reports are currently provided via Acacia's web application.

1. [Message Report](../messages)
2. [DOI Report](../list)

Working with Messages Report
----------------------------

The purpose of the message report is to show which messages Acacia
knows about. The retrieval of email from the [submissions.authors@library.caltech.edu](email:submissions.authors@library.caltech.edu) account is
done automatically throughout the day. This report shows what messages
have been retrieved and on what day they were retrieved. It also
includes a column "Processed". If you see a ✔️ in the column that means
the message was processed and any DOI found has been extracted and
placed into the DOI Report.


Working with the DOI Report
---------------------------

The DOI Report shows the DOI that Acacia knows about and the status
of processing that DOI. The first step for new DOI is indicated by the
a status of "pending" and a button labeled "look up". For each DOI with
a the "look up" button press the button. This will cause Acacia to then
check CrossRef and DataCite for any metadata available for that DOI and
if available generate appropriate EPrints XML.

The second step is taken when you see the status of "ready".
If ready you should see a link for EPrints XML. Click the link and download
the EPrints XML for the DOI. Also download PDFs from either the DOI link or URL to PDF link (if available).  

The third step is to take the EPrints XML and downloaded PDF and import them into [CaltechAUTHORS](https://authors.library.catech.edu) like you would using the `doi2eprintsxml` tool.

Once you've imported the material successfully into EPrints switch back to 
Acacia's [DOI Report](../list) and press the "remove" button on the row with the DOI you just imported.

<div class="paging">

Continue Reading
----------------

- [Up](./ "Table of Contents")
- [Next](export-to-eprints.html "Export submissions to EPrints")
- [Prev](retrieving-metadata.html "Retrieving metadata from CrossRef DataCite")

</div>
