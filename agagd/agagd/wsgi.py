"""
WSGI config for agagd project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agagd.settings.prod")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application

agagd_environ_keys = [
    "DJANGO_SETTINGS_MODULE",
    "GOOGLE_ANALYTICS_TRACKING_ID",
    "AGAGD_USER",
    "MYSQL_PASS",
    "APP_DB_NAME",
    "DB_HOST",
    "DB_PORT",
    "SECRET_KEY",
    "PROJECT_ROOT",
    "TEMPLATE_DIR",
]


def application(env, start_response):
    if all(key in env for key in agagd_environ_keys):
        os.environ[key] = env[key]
    _application = get_wsgi_application()
    return _application(env, start_response)
