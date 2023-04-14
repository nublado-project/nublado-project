#!/usr/bin/env bash
pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input

if [[ $CREATE_SUPERUSER ]];
then
  python manage.py createsuperuser --no-input
fi
