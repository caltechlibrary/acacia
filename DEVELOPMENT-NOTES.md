Development Notes
=================

This site is built using the concept that "content" is most of the site
and that additional functionality is provided by very light wait services.
This means the first building block of this web application is markdown
used to generate web forms, some templates as well as all "static" pages.
At initially stage of development only HTML and CSS are used for UI construction.

Forms
-----

If you needs to edit the one "form" and response you should edit the Markdown content in the `forms` folder. Pandoc is the rendering engine for Markdown. For the HTML form elements to be left alone you need to start HTML elements at the start of each line. If you indent before starting the element the greater than and less than symbols will be converted into HTML entities.

Templates
---------

The following templates are generated from Markdown

- templates/nav.tpl
- templates/add-doi.tpl
- tempaltes/doi-submitted.tpl

