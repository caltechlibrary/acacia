Acacia -- Overview
==================

Acacia is a system for managing submissions of DOI for
[CaltechAUTHORS](https://authors.library.caltech.edu) currently
an EPrints Repository. The purpose of Acacia is to encourage content
submissions by requiring a minimum of information. That minimum is
currently set as the DOI and URL to the digital object identified
by the DOI.

These simple submission requirements allow for easy inguest of
content by using of EMail or simple web forms. For EMail submissions
a person or form sends a message to
[submissions.authors@library.caltech.edu](email:submissions.authors@library.caltech.edu). In the text (body) of the message they need to
include one or more lines starting  with a DOI, followed by
a pipe symbol and URL to the digital object. The pipe and
URL maybe omitted.

Acacia includes a process that regularly checks the email address
above and processes new emails retrieving the metadata of the
DOI. This submitted DOI can then be reviewed by Library Staff
via a web application hosted on apps.library.caltech.edu.
Submissions can then be exported for ingest into EPrints 
via EPrints XML or flagged for removal.


Email Submissions
-----------------

Only lines that start with a DOI are processed. All other lines
are ignored. The URL to the object is optional though highly recommended.
You input a pipe symbol "`|`" between the DOI and URL. The end of line
delimits between submissions. One email can contain many submissions.

### Example email submissions


A hand typed email used to DOI the submission process:

```
This is a test message for processing DOI

10.1007/bfb0106626 <https://doi.org/10.1007/bfb0106626>

Just a test,

From R. S. Doiel account
```

An example of an ACM Open submission:

```
10.1007/BF02547335 | https://link.springer.com/content/pdf/10.1007/BF02547335.pdf

10.1090/S0002-9939-97-03559-4 | https://www.ams.org/journals/proc/1997-125-01/S0002-9939-97-03559-4/S0002-9939-97-03559-4.pdf

10.1090/S0002-9939-97-03726-X | https://www.ams.org/journals/proc/1997-125-05/S0002-9939-97-03726-X/S0002-9939-97-03726-X.pdf

10.1007/BF02392693 | https://link.springer.com/content/pdf/10.1007/BF02392693.pdf

10.5169/seals-117010

10.1016/0191-8141(94)90075-2 | https://reader.elsevier.com/reader/sd/pii/0191814194900752?token=B55983919101629946793E0A6056F7946CE8354B4F67536AF667C40F3A5CBA298C067F63543459264DFE1D8DBD818EA1&originRegion=us-east-1&originCreation=20210517225526

10.1016/0040-1951(92)90129-T | http://www.sciencedirect.com/science/article/pii/004019519290129T/pdf?md5=6465199ae8768412c840430a230f5525&pid=1-s2.0-004019519290129T-main.pdf

10.1016/0040-1951(92)90296-I | https://reader.elsevier.com/reader/sd/pii/004019519290296I?token=FA049D124E8379B171A51D55EC7E10024A11C19869D70ABCBF4A9D5369BBEA9B5F957B9DCB35D7D06E31EF77C1D28A44&originRegion=us-east-1&originCreation=20210517225749

10.1021/ja982536e | https://pubs.acs.org/doi/pdf/10.1021/ja982536e

10.1021/ja964472i | https://pubs.acs.org/doi/pdf/10.1021/ja964472i
```


