#!/bin/env python

from base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

_user = os.environ['AGAGD_USER']
_password = os.environ['MYSQL_PASS']
_key = os.environ['SECRET_KEY']

SECRET_KEY = _key

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'agagd',                      # Or path to database file if using sqlite3.
        'USER': _user,                      # Not used with sqlite3.
        'PASSWORD': _password,                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
