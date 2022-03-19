.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

==========
BrokenURLs
==========

    A simple crawler looking for 404 resources

==========
How to install
==========
"""
Run ``pip3 install -r requirements.txt .``
which will install the command ``brokenUrls`` inside your current environment.

You may be asked for adding the folder containing bin files to your $PATH

just a couple of examples:
``export PATH=$PATH:/usr/local/bin``
or
``export PATH=$PATH:/usr/bin``

"""

==========
Usage
==========
Run ``brokenUrls -h`` for options provided

Run ``brokenUrls -u https://mywebsite.com/`` to execute a scan

Run ``brokenUrls -u https://mywebsite.com/ -imgOnly`` to execute a scan searching only for broken images' urls (PNG,JPG,JPEG,SVG)

.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.2.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
