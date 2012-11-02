Introduction
============

The Django-Social-User library provides an abstract Django-based system for working with remote social networks identities. A social identity stores all information gathered about a person from a social network account, and attempts to mirror the information that is necessary for a Django user.

All functions and classes are documented inline. If you have additional questions, I can be reached on github or at admin@mattsnider.com.

Getting started
===============

Standard stuff applies to install. Use PIP to install with dependencies:

    pip install git+https://github.com/mattsnider/Django-Social-User.git#egg=django_social_user

Or install from the command line:

    python setup.py install

Dependencies
============

This library is dependent on Django 1.3 or greater. You will need to configure any remote services that you wish to use as this library is expected to be extended. I have a second project django-simple-social (https://www.github.com/mattsnider/django-simple-social) that uses this package to interface with common social networks.

If you have south installed, then database table creation and future updates will be managed automatically. If you don't, you may run into DB compatibility issues that you must manually resolve.

Usage Guide
===========



Todo
====

#. better error handling