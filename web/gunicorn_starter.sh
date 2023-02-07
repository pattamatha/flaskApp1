#!/bin/sh

if [ "$FLASK_ENV" = "development" ]; then
    echo "Creating the database tables..."
    python3 manage.py create_db
    python3 manage.py seed_db
    echo "Tables created"
fi

gunicorn main:app -c "$PWD"/gunicorn.config.py