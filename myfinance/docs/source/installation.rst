============
Installation
============

A point-by-point set of instructions on how to onboardyourself or another developer with the 
software setup for aproject.

Considering the order, follow the instructions below.

VirtualEnv
==========

You should create a new virtual environment and install the requirements::

    virtualenv virtualenv_path/pdi
    source virtualenv_path/bin/activate
    cd myfinance
    pip install -r requirements.pip

Database setup
==============

You ougth create a database::

    python manage.py syncdb

Runserver
=========

To turn it on you have to start the webserver::

    python manage.py runserver


Access
======
You can have access to the Purchase Data Importer through this url: http://127.0.0.1:8000/purchase/pdi/
