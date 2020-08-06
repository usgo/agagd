#!/bin/bash

# This is sugar to allow our docker-config to use the same variable name for the app
# and for the mysql server itself.
export MYSQL_PASS=$MYSQL_PASSWORD

MYSQL_COMMAND="mysql --host=$DB_HOST --port=$DB_PORT --user=$AGAGD_USER --password=$MYSQL_PASSWORD"

# Wait on DB server to be up *and* app DB to be created and available.
function wait_for_db() {
    let attempt=1

    while [ $attempt -le 15 ]; do
        echo "Attempting to connect to database. (attempt $attempt of 15)"
        if $MYSQL_COMMAND $APP_DB_NAME -e "describe top_kyu_view" > /dev/null; then
            echo "Database available. Continuing."
            return
        fi
        sleep 10
        let attempt++
    done

    # If we reach here, we have failed to connect.
    echo "Couldn't connect to database. Giving up."
    exit 1
}

wait_for_db

if $LOAD_FIXTURES == "true"; then
    python manage.py loaddata fake_data
fi

uwsgi --http-socket 0.0.0.0:3031 --module agagd.wsgi --static-map /static=/tmp/static/
