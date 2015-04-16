# pdf-auto-rotate
script that rotates pdf documents to portrait

This is a python script that rotates pages in PDF document so that all the pages
are portrait.

It requires pdftk to run.

Depending on version of pdftk you might need to change the line:
```python
        to_rotate.append('E')
```
to:
```python
        to_rotate.append('east')
```
because pdftk developers changed the syntax at some point (probably version
1.45).
