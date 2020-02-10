# Running agagd locally via docker

## Overview

Docker can automate much of the configuration for you.


## Using docker

### Prerequisites

* Recent versions of `docker` and `docker-compose`.
* A database dump of the full AGAGD schema, stored at `schema.sql`. (in the root directory of the repository)

### Running a dev environment using Docker

Create the file `config-docker.env` (in the repository root) and populate it with the following values:

~~~
MYSQL_PASSWORD=some-password
MYSQL_ROOT_PASSWORD=some-other-password
~~~

These values will be used by both the database and the app. Now, run:

~~~
$ docker-compose build
$ docker-compose up
~~~

Wait for the database to initialize and the app to start up. (there will be something like `spawned uWSGI worker` in the logs)

You should now be serving the app at http://localhost:8000.


### Caveats

* New changes will only be picked up when you run `docker-compose build` and then re-run `docker-compose up`.
* The database/tables will persist between builds and runs. If you need to clear out the database and start over from scratch, run `docker-compose down` and then `docker volume rm agagd_database`.
* By default, the fake_data fixture data will be re-installed on every run of the app. This may erase any local changes you made previously. To disable this functionality, you can create a `docker-compose.override.yml` file and set `LOAD_FIXTURES` to `"false"`. See the [docker-compose documentation](https://docs.docker.com/compose/extends/#understanding-multiple-compose-files) for more information on overriding docker-compose values.
