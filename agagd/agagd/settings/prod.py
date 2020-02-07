#!/bin/env python

from base import *

if os.getenv('DEBUG') == 'true':
  DEBUG = True
else:
  DEBUG = False

TEMPLATE_DEBUG = DEBUG
ADMIN_ENABLED = False

_user = os.environ['AGAGD_USER']
_password = os.environ['MYSQL_PASS']
_key = os.environ['SECRET_KEY']
_dbname = os.environ['APP_DB_NAME']
_dbhost = os.getenv('DB_HOST', '')
_dbport = os.getenv('DB_PORT', '')
#_templates = os.environ['TEMPLATE_DIR']

SECRET_KEY = _key

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': _dbname,                      # Or path to database file if using sqlite3.
        'USER': _user,                      # Not used with sqlite3.
        'PASSWORD': _password,                  # Not used with sqlite3.
        'HOST': _dbhost,                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': _dbport,                      # Set to empty string for default. Not used with sqlite3.
    }
}

#TEMPLATE_DIRS = (_templates, )
