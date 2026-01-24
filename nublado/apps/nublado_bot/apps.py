import logging

from django.apps import AppConfig
from django.conf import settings

from django_telegram.bot_registry import registry

from .bot import create_app

logger = logging.getLogger("django")
BOT_NAME = settings.NUBLADO_BOT


class NubladoBotConfig(AppConfig):
    name = "nublado_bot"

    def ready(self):
        registry.register(BOT_NAME, create_app())
