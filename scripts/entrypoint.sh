#!/bin/bash

# Get the r_flag from the options.
while getopts ':r' flag; do
    case ${flag} in
      r)
        get_options_r_flag=0
        ;;
    esac
done

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

wait_for_db

# Start the server by default without py-autoload.
# If the r argument is supplied as in development,
# autoreload the server on py file changes.
function start_server() {
    r_flag=${get_options_r_flag:-1}

    if [ $r_flag == 0 ];
    then
      python manage.py runserver 0.0.0.0:8000
    elif [ $r_flag == 1 ];
    then
      gunicorn -b 0.0.0.0:8000 agagd.wsgi
    fi
}

if $LOAD_FIXTURES == "true"; then
    python make_fake_fixtures.py 1000 1000 1000 > /tmp/fake_agagd_data.json
    python manage.py loaddata /tmp/fake_agagd_data.json
fi

# Run Collect Static in the Entrypoint because Dockerfile does not always
# get all static images. For example, debug toolbar will not have css, images or
# other assets shown.
python manage.py collectstatic --noinput

start_server
