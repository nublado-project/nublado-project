#!/usr/bin/env bash

pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py migrate django_telegram users
python manage.py collectstatic --no-input

if [[ $CREATE_SUPERUSER = true ]];
then
  python manage.py createsuperuser --no-input
fi
