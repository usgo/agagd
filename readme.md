
# AGAGD

## Overview
An app to display users, games, and tournaments on the AGA website.


## Development

### Getting started

Virtualenv and virtualenvwrapper are recommended.  It should be as easy as:

~~~
$ workon agagd # set up the virtualenv
$ pip install django django-admin-tools

[ ... monkey about with db settings ... ]

$ python manage.py runserver
~~~

### Roadmap

1. Get a basic set of models & views working with the existing DB.
2. Focus on the views around viewing player cards and their game history
3. Get the tournament/wall list re-creation features up.
4. ...
5. Declare victory

