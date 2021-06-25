# Running agagd locally via docker

## Overview

Docker packages software into virtual containers so it can run on any Linux, Windows, or macOS computer. It can automate much of the configuration for you.

## Using docker

### Prerequisites

- Recent versions of `docker` and `docker-compose`.
- A database dump of the full AGAGD schema, stored at `schema.sql`. (in the root directory of the repository)

#### [Installation](https://docs.docker.com/engine/install)

##### Mac & Windows

Installing the [Docker Desktop](https://www.docker.com/products/docker-desktop) application is highly recommended.

##### Linux

The Docker Engine is available on a variety of Linux platforms:

- [CentOS](https://docs.docker.com/engine/install/centos/)
- [Debian](https://docs.docker.com/engine/install/debian/) (and Debian derivatives)
- [Fedora](https://docs.docker.com/engine/install/fedora/)
- [Ubuntu](https://docs.docker.com/engine/install/ubuntu/) (and Ubuntu derivatives)

##### Static Binary Installation

If you're not on a supported platform, you can install from [static binaries](https://docs.docker.com/engine/install/binaries/).

### Running a dev environment using Docker

If you wish to change the environmental variables, the `.env` file to provides values for the environmental variables. Additional information about how docker-compose uses env-files can be found on [Environmental File](https://docs.docker.com/compose/env-file/).

These values will be used by both the database and the app. Now, run either:

#### For Python 2.7

```
$ docker-compose up --build
```

#### For Python 3.7

##### Note: Python 3.7+ is not fully supported by the AGAGD Application. More information can be found in issue #112.

```
$ docker-compose -f docker-compose.yml up --build
```

Wait for the database to initialize and the app to start up. (there will be something like `spawned uWSGI worker` in the logs)

You should now be serving the app at http://localhost:8000.

### Caveats

- New changes will only be picked up when you re-build the container, e.g. with `docker-compose up --force-recreate --build`.
- The database/tables will persist between builds and runs. If you need to clear out the database and start over from scratch, run `docker-compose down` and then `docker volume rm agagd_database`.
- By default, the fake_data fixture data will be re-installed on every run of the app. This may erase any local changes you made previously. To disable this functionality, you can create a `docker-compose.override.yml` file and set `LOAD_FIXTURES` to `"false"`. See the [docker-compose documentation](https://docs.docker.com/compose/extends/#understanding-multiple-compose-files) for more information on overriding docker-compose values.
