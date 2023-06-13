#!/bin/bash

cd /app/cars

gunicorn --bind :$PORT --workers 2 --threads 8 --timeout 0 cars.wsgi:application