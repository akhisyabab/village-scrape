#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z engine-db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"
python manage.py db upgrade
gunicorn --bind :5000 manage:app
