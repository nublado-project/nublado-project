import json
import logging

from telegram import Update

from django.http import Http404, JsonResponse, HttpResponse
from django.views import View

from .apps import DjangoTelegramConfig

logger = logging.getLogger('django')


class BotSetWebhookView(View):
    async def post(self, request, *args, **kwargs):
        bot_id = kwargs['bot_id']
        bot = DjangoTelegramConfig.bot_registry.get_bot(bot_id)

        if bot is not None:
            try:
                await bot.set_webhook()
                logger.info(f"Webhook for bot {bot.name} set successfully in view.")
                return JsonResponse({})
            except Exception as e:
                logger.error(f"Error in setting up webhook for bot {bot.name}: {e}")
                raise Http404
        else:
            logger.error(f"Requested bot {bot_id} not found.")
            raise Http404


class BotWebhookView(View):
    async def post(self, request, *args, **kwargs):
        bot_id = kwargs['bot_id']
        bot = DjangoTelegramConfig.bot_registry.get_bot(bot_id)

        if bot is not None:
            try:
                data = json.loads(request.body.decode('utf-8'))
            except Exception as e:
                logger.error(f"Error in decoding update: {e}")
                raise Http404
            try:
                # await bot.application.update_queue.put(
                #     Update.de_json(data=json.loads(request.body), bot=bot.application.bot)
                # )
                update = Update.de_json(data, bot.telegram_bot)
                #async with bot.application:
                await bot.application.process_update(update)
            except Exception as e:
                logger.error(f"Error in processing update: {e}")
                raise Http404
            #return JsonResponse({})
            return HttpResponse()
        else:
            raise Http404
