
Action Items
============

next
----

**Automated processing**

- [x] Figure out how to connect from Python to Google SMTP service to read the submissions.authors@library.caltech.edu. According to the configuration in Thunderbird OAuth2 is being used to authenticate.
- [x] Rename email to messages, people to persons
- [x] Sort out models for message, DOI request and retrieval records
- [x] Implement an automated mail fetch (run from cron)
- [x] Implement email to DOI request process (run from cron)
- [x] Implement DOI request to retrieval process (run from cron)
    - currently via SSH and a script on the old EPrints box
    - [x] Test EPrintsSSH to see if I can retrieve valid EPrints id

**Staff managed processing**

- [ ] Documentation cleanup
    - [ ] Proofread and copyedit
    - [ ] Organize documentation around activities
    - [ ] Improve installation instructures
    - [ ] Writeup idea map for future versions
- [x] Need `BASE_URL` integrating into settings.ini and in mk-static-pages.bash.
    - On dev box app is in root but in production it'll be under the "/acacia/" directory
    - Also need to handle base url in pandoc and bottler templates
- [x] Create a dashboard page for linked to tasks
    - [x] Inbox (Retrieve submissions.author emails)
        - [x] Provide a means of triggering `get-messages` script
        - [x] Provide a means of triggering `messages-to-doi` script
        - [x] Provide a way to clear the message table
        - [x] List contents retrieved from email account
    - [ ] Process DOI
        - [x] Show link to DOI
        - [x] Show link Object URL if provided
        - [x] Show status or EPrint URL if eprint record exists
        - [x] Show link to retrieved EPrints XML
        - [ ] Provide a means of triggering `retrieve-metadata` script
        - [ ] Provide a means to retrieve the individual DOI records
        - [x] Provide button to move to trash/processed
        - [x] List contents DOI queued in Acacia


