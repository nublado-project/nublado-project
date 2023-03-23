import json
import logging

from telegram import Update

from django.http import Http404, JsonResponse
from django.views import View

from .apps import DjangoTelegramConfig

logger = logging.getLogger('django')


class BotSetWebhookView(View):
    async def post(self, request, *args, **kwargs):
        token = kwargs['token']
        bot = DjangoTelegramConfig.bot_registry.get_bot(token)

        if bot is not None:
            try:
                await bot.start_webhook()
                logger.info(f"Webhook for bot {bot.token} set successfully in view.")
                return JsonResponse({})
            except Exception as e:
                logger.error(f"Error in setting up webhook for bot {bot.token}: {e}")
                raise Http404
        else:
            logger.error(f"Requested bot {token} not found.")
            raise Http404


class BotWebhookView(View):
    async def post(self, request, *args, **kwargs):
        token = kwargs['token']
        bot = DjangoTelegramConfig.bot_registry.get_bot(token)

        if bot is not None:
            try:
                data = json.loads(request.body.decode('utf-8'))
            except Exception as e:
                logger.error(f"Error in decoding update: {e}")
                raise Http404
            try:
                update = Update.de_json(data, bot.telegram_bot)
                async with bot.application:
                    await bot.application.process_update(update)
            except Exception as e:
                logger.error(f"Error in processing update: {e}")
            return JsonResponse({})
        else:
            raise Http404
