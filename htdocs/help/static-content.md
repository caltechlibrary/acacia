Static Content
==============

Much of the Acacia application is generated from Markdown files.
This includes both HTML pages and some templates for navigation.

Updating the static content means editing the Markdown source files
and running the GNU make. This will run a script called `mk-static-pages.bash` which in turn uses [Pandoc](https://pandoc.org) and [MkPage](https://github.com/caltechlbirary/mkpage) to render the pages and templates.

If you want to force remake the static content and templates run

```
make clean
make
```

<div class="paging">

Continue Reading
----------------

- [Up](developers.html "Developer documentation")
- [Prev](people-manager.html "People Manager")

</div>

