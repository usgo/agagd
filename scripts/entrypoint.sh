#!/bin/bash

# Cause the script to fail loudly when it fails.
# see: (http://redsymbol.net/articles/unofficial-bash-strict-mode/)
set -euo pipefail

# Set the MySQL Command
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

if [[ "$3" != "test" ]]; then
  wait_for_db
fi

if $LOAD_FIXTURES == "true"; then
    python make_fake_fixtures.py 1000 1000 1000 > /tmp/fake_agagd_data.json
    python manage.py loaddata /tmp/fake_agagd_data.json
fi

# Run Collect Static in the Entrypoint because Dockerfile does not always
# get all static images. For example, debug toolbar will not have css, images or
# other assets shown.
python manage.py collectstatic --noinput

# Allow the commands to be passed into Entrypoint.
exec "$@"
