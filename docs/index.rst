.. bublfish documentation master file, created by
   sphinx-quickstart on Sun Nov  2 17:15:16 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to bublfish's documentation!
====================================

Contents:

.. toctree::
   :maxdepth: 2

   user
   comment

General response
================

OK::

    {
        "status": 200,
        "data": {}
    }

ERROR::

    {
        "status": 500,
        "data": {},
        "info": "机房断电啦"
    }

Status code
===========

    200: OK

    400: Bad request data

    403: Need login

    500: System error

Jsonp
=====

    You can add a ``callback`` in GET or POST in every api.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

