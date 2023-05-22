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

    def ready(self):
        self.setup_bots()