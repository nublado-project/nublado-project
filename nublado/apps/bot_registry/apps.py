import logging

from django.apps import AppConfig


logger = logging.getLogger("django")


class BotRegistryConfig(AppConfig):
    name = "bot_registry"