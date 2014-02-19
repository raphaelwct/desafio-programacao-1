Tests
=====

This project was developed using TDD and BDD methodologies, below are some instructions to run the
project's tests.

First of all, start the web server::

    python manage.py runserver

To run the functional tests, do the following::

    behave purchase/tests/features

To run the unit tests::

    python manage.py test purchase 
