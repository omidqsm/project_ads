#!/bin/bash

echo "create migration files if not existing"
pipenv run python manage.py makemigrations

echo "Apply database migrations"
pipenv run python manage.py migrate

echo "Starting server"
pipenv run rundev 0.0.0.0:8000
