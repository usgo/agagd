
# The American Go Association Games Database (AGAGD)

The `AGAGD` application is what runs [agagd.usgo.org](https://agagd.usgo.org). Originally, ported from the EuroGo Games Database, the `AGAGD` application provides a means for members and non-members tournament information, chapter information and member insights.

## Contents

* [Contributing](#contributing)
* [Requirements](#requirements)
* [Getting Started](#getting_started)
* [Triage](#triage)
* [Caveats](#caveats)
* [License](#license)

## Contributing

We welcome any contributions. You could update documentation or our getting started or add a feature or find another way to improve the `AGAGD` application. Any contributions should be submitted as Pull Requests (PR) with [Conventional Commit(s) Messages](https://www.conventionalcommits.org). You can use the [CZ Cli](https://github.com/commitizen/cz-cli) tool if you would like a conventional commit message aid.

If you new to contributing on Github, take a look a the [First Contributions](https://firstcontributions.github.io/) project.

## Requirements

The `ÀGAGD` application uses Docker Compose and containers for local development. As such, we require that you have Docker and Docker compose installed on your system. To run our `AGAGD` application you currently need a `schema.sql` from the repository [usgo-sql-schemas](https://github.com/usgo/usgo-sql-schemas/blob/main/schema.sql).

## Getting Started

### Pre-Requisites

* [Git](https://git-scm.com/)
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)
* [schema.sql](https://github.com/usgo/usgo-sql-schemas/blob/main/schema.sql)

### Get a local copy of `schema.sql`

`$ curl -sSL https://raw.githubusercontent.com/usgo/usgo-sql-schemas/main/schema.sql -o schema.sql`

### Run the `AGAGD` application using

`$ docker-compose up`

### Run tests for the `AGAGD` application using

`$ docker-compose -f docker-compose.test.yml run test_app`

### The `AGAGD` app should now be running at

[http://localhost:8000](http://localhost:8000)

## Triage

[Bug Triage](https://github.com/usgo/agagd/projects/1) project for the AGAGD which lists and organizes current priorites the AGA Development Team has for the AGAGD.

## Caveats

* By default, the fake_data fixture data will be re-installed on every run of the app. This may erase any local changes you made previously. To disable this functionality, you can create a `docker-compose.override.yml` file and set `LOAD_FIXTURES` to `"false"`. See the [docker-compose documentation](https://docs.docker.com/compose/extends/#understanding-multiple-compose-files) for more information on overriding docker-compose values.

## License

MIT © [American Go Association](/LICENSE)
