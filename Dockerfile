# Dockerfile for agagd application local development environment.
#
# In addition to environment variables used by the application, the entrypoint script is affected by the following. docker-compose.yml sets reasonable defaults for a development environment:
# * DB_HOST - database hostname
# * DB_PORT - database port
# * APP_DB_NAME - name of the database to use
# * AGAGD_USER - database username
# * MYSQL_PASSWORD - database password (the docker entrypoint sets MYSQL_PASS to this value for app compatibility)

FROM alpine

WORKDIR /srv

RUN apk add --no-cache \
    mysql-client \
    bash \
    py-pip \
    build-base \
    sqlite-dev \
    python-dev \
    mariadb-dev \
    linux-headers

COPY requirements.txt /srv/
RUN pip install --no-cache-dir -U pip &&\
    pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir uwsgi # docker-specific requirement

ENV PROJECT_ROOT=/srv
ENV TEMPLATE_DIR=/srv/templates

COPY scripts/entrypoint.sh /srv/
COPY agagd/ /srv/

CMD ["/srv/entrypoint.sh"]
