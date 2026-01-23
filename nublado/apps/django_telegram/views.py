import json
import logging

from telegram import Update

from django.http import JsonResponse #, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .bot_application import application, ensure_initialized


logger = logging.getLogger("django")


@csrf_exempt
async def telegram_webhook(request):
    # Optional: verify secret token
    # if (
    #     request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    #     != settings.DJANGO_TELEGRAM_WEBHOOK_SECRET
    # ):
    #     return HttpResponseForbidden("Invalid secret")

    if request.method != "POST":
        return JsonResponse({"ok": False})

    await ensure_initialized()

    data = json.loads(request.body.decode("utf-8"))
    update = Update.de_json(data, application.bot)

    await application.process_update(update)
    return JsonResponse({"ok": True})