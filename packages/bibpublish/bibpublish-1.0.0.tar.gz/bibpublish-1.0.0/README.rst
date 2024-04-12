bibPublish
==========
bibPublish uses templates for publishing BibTex bibliographies in different formats such as HTML and LaTeX::

  Usage: publish.py [options]
  
  Options:
    -h, --help            show this help message and exit
    -o OUTPUT_DIR, --output-dir=OUTPUT_DIR
                          output directory.
    -t TEMPLATE, --template=TEMPLATE
                          template to use (wordpress).
    -f FILTER, --filter=FILTER
                          one consider items that match the given
                          filter criterion.

Example
-------
Publish all BibTex entries that have been published after 2014::

  ./scripts/publish.py mybib.bib -f 'int(year) > 2014'

Supported templates
-------------------

- worpress: Template used for the Web page. Creates the publication HTML and supporting files (abstracts and bibtex fiels).
- latex: Used for integrating bibliographies into the CV


Background
----------
bibPublish is a Python 3+ compatible replacement for `bibTexSuite <https://github.com/AlbertWeichselbraun/bibTexSuite>`_.
