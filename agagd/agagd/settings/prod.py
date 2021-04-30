#!/bin/env python

from .base import *

if os.getenv("DEBUG") == "true":
    DEBUG = True

    # DebugToolbar Middleware
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

    # DebugToobar
    INSTALLED_APPS += ["debug_toolbar"]

    # DebugToolbar Configurations
    DEBUG_TOOLBAR_CONFIG = {
        "INTERCEPT_REDIRECTS": False,
        "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
    }

    # Add our Docker host IP to the INTERNAL_IPS
    import os
    import socket

    HOSTNAME = os.getenv("HOSTNAME")
    INTERNAL_IPS = [socket.gethostbyname(HOSTNAME)]
else:
    DEBUG = False


GOOGLE_ANALYTICS_TRACKING_ID = os.getenv("GOOGLE_ANALYTICS_TRACKING_ID", "")

ADMIN_ENABLED = False

# For SECRET_KEY, we want to be absolutely certain a value is provided
# explicitly by configuration to ensure secure production environment.
# Without this value we should abort.
_key = os.environ["SECRET_KEY"]

_user = os.getenv("AGAGD_USER", "")
_password = os.getenv("MYSQL_PASSWORD", "")
_dbname = os.getenv("APP_DB_NAME", "")
_dbhost = os.getenv("DB_HOST", "")
_dbport = os.getenv("DB_PORT", "")

SECRET_KEY = _key

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        "NAME": _dbname,  # Or path to database file if using sqlite3.
        "USER": _user,  # Not used with sqlite3.
        "PASSWORD": _password,  # Not used with sqlite3.
        "HOST": _dbhost,  # Set to empty string for localhost. Not used with sqlite3.
        "PORT": _dbport,  # Set to empty string for default. Not used with sqlite3.
    }
}
