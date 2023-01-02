import logging

from django.conf import settings
from django.apps import AppConfig

logger = logging.getLogger('django')


class BotMiscConfig(AppConfig):
    name = "bot_misc"