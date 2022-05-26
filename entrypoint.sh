#!/bin/bash

echo "Migrate the Database at startup of project"

until nc -z -v -w30 "$DATABASE_HOST" "$DATABASE_PORT"
do
    echo "Waiting for a database..."
    sleep 0.5
done

python manage.py migrate
python manage.py runserver 0.0.0.0:8000
