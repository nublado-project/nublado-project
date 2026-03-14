#!/usr/bin/env bash

gunicorn config.asgi:application -w 1 -k uvicorn.workers.UvicornWorker
python manage.py set_bot_webhooks

