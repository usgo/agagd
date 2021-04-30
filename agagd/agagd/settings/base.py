import os

import django.conf.global_settings as DEFAULT_SETTINGS

PROJECT_ROOT = os.environ["PROJECT_ROOT"]

# AGAGD Administrators Configuration:
#
# This assumes AGAGD_ADMINS environmental variable is formated as follows:
# 'webmaster:webmaster@usgo.org,agagd_webmaster:agagd+webmaster@usgo.org'
#
# For local configurations the ADMINS defaults to [('Admin', 'admin@localhost.local')]
ADMINS = []

if os.getenv("AGAGD_ADMINS") == None:
    ADMINS.append(("Admin", "admin@localhost.local"))
else:
    ADMINS = [
        (value.split(":")[0], value.split(":")[1])
        for value in os.environ.get("AGAGD_ADMINS").split(",")
    ]

MANAGERS = ADMINS

# Allow only the default ALLOWED_HOSTS ['.localhost', '127.0.0.1', '[::1]'].
ALLOWED_HOSTS = []

# Only one allowed host is expected here.
if os.getenv("ALLOWED_HOSTS") != None:
    ALLOWED_HOSTS.append(os.getenv("ALLOWED_HOSTS"))

# Default Interal IP Addresses for DJango.
INTERNAL_IPS = ["127.0.0.1", "[::1]"]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = "America/Chicago"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = "/tmp/static/"

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Additional locations of static files
STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, "static"),)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

MIDDLEWARE = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    # Uncomment the next line for simple clickjacking protection:
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
)

ROOT_URLCONF = "agagd.urls"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "agagd.wsgi.application"

# Changed TEMPLATES because existing template related settings are depreciated
# https://docs.djangoproject.com/en/1.11/ref/templates/upgrading/#the-templates-settings
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(PROJECT_ROOT, "templates")],
        "OPTIONS": {
            "context_processors": [
                # Standard context_processors
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                # Custom context_processors
                "django.template.context_processors.request",
                "agagd_core.context_processors.google_analytics_tracking_id",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
                # 'django.template.loaders.eggs.Loader',
            ],
        },
    },
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [os.path.join(PROJECT_ROOT, "jinja2")],
        "OPTIONS": {
            "environment": "agagd_core.jinga2.environment",
            "context_processors": [
                # Standard context_processors
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                # Custom context_processors
                "django.template.context_processors.request",
                "agagd_core.context_processors.google_analytics_tracking_id",
            ],
        },
    },
]


INSTALLED_APPS = (
    "agagd_core",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_tables2",
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        }
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        }
    },
}
