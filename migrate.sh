#!/bin/bash

cd /app/cars

./manage.py migrate
./manage.py collectstatic --noinput