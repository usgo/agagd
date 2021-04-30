# Dockerfile for agagd application local development environment.
#
# In addition to environment variables used by the application, the entrypoint script is affected by the following. docker-compose.yml sets reasonable defaults for a development environment:
# * DB_HOST - database hostname
# * DB_PORT - database port
# * APP_DB_NAME - name of the database to use
# * AGAGD_USER - database username
# * MYSQL_PASSWORD - database password (the docker entrypoint sets MYSQL_PASS to this value for app compatibility)

### Build stage, to avoid leaving dev dependencies in the final image
FROM python:3.9-slim-buster AS build

WORKDIR /build

RUN apt-get update && apt-get install -y \
    libsqlite3-dev \
    libmariadb-dev \
    build-essential
RUN pip install --no-cache-dir -U pip

COPY requirements.txt /build/
RUN pip install --user --no-cache-dir -r requirements.txt && pip install --user --no-cache-dir uwsgi

### Final image
FROM python:3.9-slim-buster

WORKDIR /srv
RUN useradd django

COPY --from=build --chown=django:django /root/.local /home/django/.local

RUN apt-get update && apt-get install -y \
    default-mysql-client \
    mime-support \
    libmariadb3

USER django

ENV PATH=/home/django/.local/bin:$PATH
ENV DJANGO_SETTINGS_MODULE=agagd.settings.prod
ENV PROJECT_ROOT=/srv
ENV TEMPLATE_DIR=/srv/templates

COPY --chown=django:django scripts/ agagd/ /srv/
RUN SECRET_KEY=stub-for-build python manage.py collectstatic --noinput

CMD ["/srv/entrypoint.sh"]
