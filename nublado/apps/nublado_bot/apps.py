import logging

from telegram.ext import CommandHandler, MessageHandler

from django.apps import AppConfig
from django.conf import settings

from django_telegram.bot_registry import registry
from django_telegram.filters import TEXT_ONLY

from .bot import create_app
from .handlers.misc import hello, start

logger = logging.getLogger("django")
BOT_NAME = settings.NUBLADO_BOT


class NubladoBotConfig(AppConfig):
    name = "nublado_bot"

    def ready(self):
        from .handlers.misc import start, hello
        from .handlers.group_points import give_points
        from .handlers.group_settings import set_bot_language

        app = create_app()
        registry.register(BOT_NAME, app)

        # Add the command handlers.
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("hello", hello))
        app.add_handler(CommandHandler("set_bot_language", set_bot_language))
        app.add_handler(MessageHandler(TEXT_ONLY, give_points))