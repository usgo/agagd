# AGAGD

## Overview
An app to display users, games, tournaments, and ratings information on the AGA website.  
A port of the old eurogo Games Database to python, for the AGA

 - agagd_core/     --
 - agagd/          -- 

## Development

### Getting started

Virtualenv and virtualenvwrapper are recommended.  It should be as easy as:

~~~
$ workon agagd # set up the virtualenv
$ pip install django django-admin-tools

[ ... monkey about with db settings ... ]

$ python manage.py runserver
~~~

### development needs
1. It'd really help if we had a sanitized version of the database we could use,
with shuffled AGAIDs, random names & chapters, and a few sample tournaments.

### Roadmap

1. Get a basic set of models & views working with the existing DB. Check!
2. Focus on the views around viewing player cards and their game history. Done!
3. Get the tournament/wall list re-creation features up. Faked!
4. Style things up nice-like. A first draft!
5. Declare victory
6. extend to put a frontend on the ratings workings of Bresler et al.
7. Provide online game submissions
8. Document game submission protocol for use with other servers.


### Deployment

This needs some help.  We'll need to diff the schema, figure out staging, 
and maybe some routing/networking magic with Steve.



