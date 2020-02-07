# AGAGD

## Overview
An app to display users, games, tournaments, and ratings information on the AGA website.  
A port of the old eurogo Games Database to python, for the AGA

 - agagd_core/     --
 - agagd/          -- 

## Development

### Getting started

**NB: agagd is no longer compatible with sqlite3; as of 2020-02-01, it requires features only available in MySQL.**

**NB: running the agagd locally now requires access to a database schema not provided by this repository.**

*A new docker-based development approach is also available, see [docker.md](docker.md) for details.*


The first step is to install `mysql` and create an `agagd` database. Then load the current database schema snapshot, as well
as the SQL files in `sql/`, into the `agagd` database, e.g.:

~~~
mysql agagd < schema.sql
for file in sql/*; do
  mysql agagd < $file
done
~~~

Next set up the app environment. Virtualenv and virtualenvwrapper are recommended.

~~~
$ mkvirtualenv agagd
$ workon agagd 
$ cd PATH_TO_REPO_ROOT
$ pip install -r requirements_dev.txt
$ cd agagd/
$ cp local_settings.py.sample local_settings.py
~~~

Edit your `local_settings.py` to match your database settings.

~~~
$ python manage.py loaddata fake_data
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



