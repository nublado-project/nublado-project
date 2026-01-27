import logging

from telegram.ext import CommandHandler, MessageHandler

from django.apps import AppConfig
from django.conf import settings

from django_telegram.bot_registry import registry
from django_telegram.filters import TEXT_ONLY

from .bot import create_app

logger = logging.getLogger("django")
BOT_NAME = settings.NUBLADO_BOT


class NubladoBotConfig(AppConfig):
    name = "nublado_bot"

    def ready(self):
        from django_telegram.policies import with_policies, GroupOnly, PrivateOnly
        from .handlers.misc import start, hello
        from .handlers.group_settings import set_bot_language
        from .handlers.group_points import give_points
        from django_telegram.utils import resolve_chat_language
        app = create_app()
        app.bot_data["language_resolver"] = resolve_chat_language
        registry.register(BOT_NAME, app)

        # Add the command handlers.
        app.add_handler(
            CommandHandler(
                "start",
                with_policies(PrivateOnly())(start),
            )
        )
        app.add_handler(
            CommandHandler(
                "hello",
                with_policies(GroupOnly())(hello),
            )
        )
        app.add_handler(
            CommandHandler(
                "set_bot_language",
                with_policies(GroupOnly())(set_bot_language),
            )
        )
        app.add_handler(
            MessageHandler(
                TEXT_ONLY,
                with_policies(GroupOnly())(give_points),
            )
        )
