Developer -- Requirements
=========================

Acacia is written in Python 3 and requires additional Python packages to work. This include the following.

```
idutils         >= 1.1.8
peewee          >= 3.14.0
python-decouple >= 3.4
mysql-connector-python >= 8.0.25
```

In addition to Python Acacia also utilizes `ssh`, `make`, `pandoc` as well as and `doi2eprintxml` in the [EPrint Tools](https://github.com/caltechlibrary/eprinttools) and `mkpage` from [MkPage](https://github.com/caltechlibrary/mkpage) projects.  Follow that project's installation instructions and adjust your `settings.ini` to correctly point to where to find `doi2eprintxml`.

<div class="paging">

Continue Reading
----------------

- [Up](./ "Table of Contents")
- [Next](commands.html "Commands")
- [Prev ](developers.html "Developer documentation")

</div>

