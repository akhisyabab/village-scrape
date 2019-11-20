#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z engine-db 5432; do
  sleep 0.1
done

python manage.py db upgrade
python manage.py runserver -h 0.0.0.0

