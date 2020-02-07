# Running agagd locally via docker

## Overview

Docker can automate much of the configuration for you.


## Using docker

### Prerequisites

* Recent versions of `docker` and `docker-compose`.
* A database dump of the full AGAGD schema, stored at `schema.sql`.

### Using Docker

Just run:

~~~
docker-compose build
docker-compose up
~~~

Wait for the database to initialize. You should now be serving the app at http://localhost:8000.


## Caveats

* New changes will only be picked up when you run `docker-compose build` and then re-run `docker-compose up`.
* The database will persist between builds. If you need to clear out the database and start over from scratch, run `docker-compose down` and then `docker volume rm agagd_database`.
