from base import *
import getpass

DEBUG = True
ADMIN_ENABLED = True

INSTALLED_APPS += ('django.contrib.admin',)

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

_password = os.environ.get('MYSQL_PASS', '')

# Make this unique, and don't share it with anybody.
SECRET_KEY = '#-+^ipw3x)1dq0$v*z0_^tzoxzcwz3s8^x8kd^5s9+9tfwuixv'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'agagd',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': _password,                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
