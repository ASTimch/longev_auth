#!/bin/sh
# run.sh

python manage.py migrate

python manage.py collectstatic --noinput

cp -r /app/collected_static/. /backend_static/

gunicorn longev_auth.wsgi --bind=0.0.0.0:8000
