#!/usr/bin/env bash

gunicorn config.asgi:application -w 4 -k uvicorn.workers.UvicornWorker
httpx https://nubladoproject.onrender.com/bot/setwebhook/${NUBLADO_BOT_TOKEN}/ -m POST
