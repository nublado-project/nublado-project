#!/usr/bin/env bash

gunicorn config.asgi:application -w 4 -k uvicorn.workers.UvicornWorker