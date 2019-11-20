#!/usr/bin/env bash
docker-compose -f docker-compose-dev.yml run engine python manage.py db upgrade
