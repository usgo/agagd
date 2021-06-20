# AGAGD

## Overview
An app to display users, games, tournaments, and ratings information on the AGA website.
The AGAGD is a port of the old EuroGO Games Database to python developed for the [American Go Association (AGA)](usgo.org).

## Development

### Code Style
The AGAGD project uses pre-commit for some basic linting and mostly follows [black](https://github.com/psf/black), so before it is required to have pre-commit installed and any errors fixed before making a pull request. ([Pre Commit](https://pre-commit.com/), [DJango Code Style](https://docs.djangoproject.com/en/3.2/internals/contributing/writing-code/coding-style/))

#### Install pre-commit
* `shell> pip3 install pre-commit`
* `shell> pre-commit install`

### Getting started

**Important: running the agagd locally now requires the `schema.sql` which can be found in [USGO SQL Schema's Repo](https://github.com/usgo/usgo-sql-schemas). The` schema.sql` file needs to be place in the main directory of the locally cloned AGAGD repo.**

The AGAGD application uses docker for local development. Information about how to get up and running see [docker.md](docker.md) for details.
