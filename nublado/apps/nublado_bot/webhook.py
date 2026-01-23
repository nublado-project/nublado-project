import json

from telegram import Update

from django.http import JsonResponse #, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from bot_registry.registry import registry

BOT_NAME = settings.NUBLADO_BOT

@csrf_exempt
async def webhook(request):
    # if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != settings.ALPHA_WEBHOOK_SECRET:
    #     return HttpResponseForbidden("Invalid secret")
    if request.method != "POST":
        return JsonResponse({"ok": False})

    await registry.ensure_initialized(BOT_NAME)

    app = registry.get(BOT_NAME)
    update = Update.de_json(json.loads(request.body.decode("utf-8")), app.bot)

    await app.process_update(update)
    return JsonResponse({"ok": True})