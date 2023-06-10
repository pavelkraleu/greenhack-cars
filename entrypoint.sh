#!/bin/bash

cd /app/cars

./manage.py migrate
./manage.py collectstatic --noinput
gunicorn --bind :$PORT --workers 2 --threads 8 --timeout 0 cars.wsgi:application