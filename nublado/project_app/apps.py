import logging

import httpx

from django.apps import AppConfig
from django.conf import settings

from django_telegram.bot import Bot
from core.utils import remove_lead_and_trail_slash

logger = logging.getLogger('django')


class ProjectAppConfig(AppConfig):
    name = "project_app"

    def setup_bots(self):
        from django_telegram.apps import DjangoTelegramConfig
        from .bots.nubladobot.bot import NubladoBot
        nublado_bot = NubladoBot(settings.NUBLADO_BOT_TOKEN, name=settings.NUBLADO_BOT)
        bot_registry = DjangoTelegramConfig.bot_registry
        bot_registry.add_bot(nublado_bot.token, nublado_bot)

        dt = settings.DJANGO_TELEGRAM
        if dt['mode'] == settings.BOT_MODE_WEBHOOK:
            from django_telegram.apps import DjangoTelegramConfig

            for token, bot in bot_registry.bots.items():
                set_webhook_site = remove_lead_and_trail_slash(dt['webhook_site'])
                set_webhook_path = remove_lead_and_trail_slash(dt['set_webhook_path'])
                set_webhook_url = f"{set_webhook_site}/{set_webhook_path}/{bot.token}/"
                logger.info(set_webhook_url)
                r = httpx.post(set_webhook_url, data={})

    def ready(self):
        self.setup_bots()