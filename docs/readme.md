# AGAGD

## Overview
An app to display users, games, tournaments, and ratings information on the AGA website.  
A port of the old eurogo Games Database to python, for the AGA

 - agagd_core/     --
 - agagd/          -- 

## Development

### Getting started

The first optional step is to install `mysql` and create an `agagd` database.

The other option is to use sqlite3.  This option doesn't require you to do anything extra.

Virtualenv and virtualenvwrapper are recommended.

~~~
$ mkvirtualenv agagd
$ workon agagd 
$ cd PATH_TO_REPO_ROOT
$ pip install -r requirements_dev.txt
$ cd agagd/
$ cp local_settings.py.sample local_settings.py
~~~

Edit your `local_settings.py` to match your database settings.  If you are using sqlite3, you don't need to change anything.

~~~
$ python manage.py syncdb --noinput
$ # python manage.py loaddata NONEXISTENT_FIXTURE - TODO
$ python manage.py runserver
~~~

After the above, you should be able to see the site up and running at http://localhost:8000

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



