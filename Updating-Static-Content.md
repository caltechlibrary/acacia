Updating Static Content
=======================

In many of the application developed at Caltech Library you can
regerate static content using `make` via `make website`. This
does not work with Acacia. The `Makefile` is primarily for building
a release via GitHub's releases process.  To rebuild the static
content of the Acacia application (i.e. the html files in htdocs)
you need to use the Bash script, `mk-static-pages.bash`.

It is important to know you need to have Pandoc installed on the
system. Pandoc is used extensively to convert the Markdown files
into HTML pages complete with all the necessary display elements.

Example usage
-------------

```bash
    ./mk-static-pages.bash
```

The script `mk-static-pages.bash` will use `page.tmpl` to generate
the related HTML files found for each Markdown document.

