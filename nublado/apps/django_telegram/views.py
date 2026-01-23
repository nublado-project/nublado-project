import json
import logging

from telegram import Update
from django.http import JsonResponse
# from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# from .apps import DjangoTelegramConfig
from .bot_application import application, ensure_initialized

logger = logging.getLogger("django")


@csrf_exempt
async def telegram_webhook(request):
    # Optional: verify secret token
    # if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != settings.DJANGO_TELEGRAM_WEBHOOK_SECRET:
    #     return HttpResponseForbidden("Invalid secret")
    if request.method != "POST":
        return JsonResponse({"ok": False})
    await ensure_initialized()
    data = json.loads(request.body.decode("utf-8"))
    update = Update.de_json(data, application.bot)

    await application.process_update(update)
    return JsonResponse({"ok": True})


# class BotSetWebhookView(View):
#     async def post(self, request, *args, **kwargs):
#         bot_id = kwargs["bot_id"]
#         bot = DjangoTelegramConfig.bot_registry.get_bot(bot_id)

#         if bot is not None:
#             try:
#                 await bot.set_webhook()
#                 logger.info(f"Webhook for bot {bot.name} set successfully in view.")
#                 return JsonResponse({})
#             except Exception as e:
#                 logger.error(f"Error in setting up webhook for bot {bot.name}: {e}")
#                 raise Http404
#         else:
#             logger.error(f"Requested bot {bot_id} not found.")
#             raise Http404


# class BotWebhookView(View):
#     async def post(self, request, *args, **kwargs):
#         bot_id = kwargs["bot_id"]
#         bot = DjangoTelegramConfig.bot_registry.get_bot(bot_id)

#         if bot is not None:
#             try:
#                 data = json.loads(request.body.decode("utf-8"))
#             except Exception as e:
#                 logger.error(f"Error in decoding update: {e}")
#                 raise Http404
#             try:
#                 update = Update.de_json(data, bot.telegram_bot)
#                 async with bot.application:
#                     await bot.application.process_update(update)
#                     # await bot.application.update_queue.put(
#                     #     Update.de_json(data=json.loads(request.body), bot=bot.application.bot)
#                     # )
#             except Exception as e:
#                 logger.error(f"Error in processing update: {e}")
#                 raise Http404
#             # return JsonResponse({})
#             return HttpResponse()
#         else:
#             raise Http404
