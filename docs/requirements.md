Acacia Requirements
===================

Acacia is written in Python 3 and requires additional Python packages to work. This include the following.

```
idutils         >= 1.1.8
peewee          >= 3.14.0
python-decouple >= 3.4
mysql-connector-python >= 8.0.25
```

In addition to Python Acacia also utilizes `ssh` and `doi2eprintxml`.
The later is avialable in the [EPrint Tools](https://github.com/caltechlibrary/eprinttools) project.  Follow that project's installation instructions
and adjust your `settings.ini` to correctly point to where to find
`doi2eprintxml`.
