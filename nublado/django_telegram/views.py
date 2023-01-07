import json
import logging

from telegram import Update
from telegram.error import TelegramError

from django.http import Http404, JsonResponse
from django.views import View

from .apps import DjangoTelegramConfig

logger = logging.getLogger('django')


class BotWebhookView(View):
    def post(self, request, *args, **kwargs):
        token = kwargs['token']
        bot = DjangoTelegramConfig.bot_registry.get_bot(token)

        if bot is not None:
            try:
                data = json.loads(request.body.decode('utf-8'))
            except Exception as e:
                error = "Error in decoding update: {e}".format(e)
                logger.error(error)

                raise Http404

            try:
                update = Update.de_json(data, bot.telegram_bot)
                bot.dispatcher.process_update(update)
            except Exception as e:
                error = "Error in processing update: {e}".format(e)
                logger.error(error)

            return JsonResponse({})
        else:
            raise Http404
