Introduction
============

The Django-Social-User library provides an abstract Django-based system for working with remote social network identities. A social identity stores all information gathered about a person from a social network account, and attempts to mirror the information that is necessary for a Django user.

All functions and classes are documented inline. If you have additional questions, I can be reached on github or at admin@mattsnider.com.

Getting started
===============

Standard stuff applies to install. Use PIP to install with dependencies:

    pip install django-social-user

Or install from the command line:

    python setup.py install

Dependencies
============

This library is dependent on Django 1.3 or greater. You will need to configure any remote services that you wish to use as this library is expected to be extended. I have a second project django-simple-social (https://www.github.com/mattsnider/django-simple-social) that uses this package to interface with common social networks.

If you have south installed, then database table creation and future updates will be managed automatically. If you don't, you may run into DB compatibility issues that you must manually resolve.

Usage Guide
===========

This section describes how to configure the Django Social User app.

URL Setup
---------

Your project should define the following URLs in your settings files:

    DJANGO_SOCIAL_USER_OPTIONS = {
        'REDIRECT_ON_ACCESS_TOKEN_FAILURE': '/yourAccessTokenFailureUrl',
        'REDIRECT_ON_AUTHENTICATION': '/yourAuthenticationUrl',
        'REDIRECT_ON_REQUEST_TOKEN_FAILURE': '/yourRequestTokenFailureUrl',
    }

REDIRECT_ON_ACCESS_TOKEN_FAILURE is where to redirect the user if a network fails to authenticate when the social network executes the callback URL.

REDIRECT_ON_AUTHENTICATION is where to redirect the user when they successfully authenticate with the social network. If this constant is not defined user will never successfully authenticate.

REDIRECT_ON_REQUEST_TOKEN_FAILURE is where to redirect the user if a network fails to provide the request URL as part of the oauth handshake (user will not have been redirected to the social network site yet, and usually means the site authentication is down or request timed out).

Add the following URL definitions to the project ``urls.py``:

    url(r'^social/', include('django_social_user.urls', namespace='django_social_user')),

DB Setup
--------

If you are using South, then run:

    python manage.py migrate django_social_user

Otherwise run:

    python manage.py sqlall django_social_user > temp.sql
    python manage.py dbshell < temp.sql
    rm temp.sql

I recommend using South, as I may need to make model changes and South migrations will make your life easier.

Create a Backend for a Social Network
-------------------------------------

I have another project called Django Simple Social that builds upon Django Social User to support some of the more popular social networks. If you plan on implementing your own social network backend, see https://github.com/mattsnider/django-simple-social for examples on how to do this.


Todo
====

1. better error handling
2. TESTING