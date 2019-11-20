#!/usr/bin/env bash
docker-compose -f docker-compose-prod.yml run engine python manage.py db migrate
