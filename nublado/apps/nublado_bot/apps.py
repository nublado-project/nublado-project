import logging

from telegram.ext import CommandHandler, MessageHandler

from django.apps import AppConfig
from django.conf import settings

from django_telegram.bot_registry import registry
from django_telegram.filters import TEXT_ONLY
from django_telegram.decorators import with_language, with_policies

from .bot import create_app

logger = logging.getLogger("django")
BOT_NAME = settings.NUBLADO_BOT


class NubladoBotConfig(AppConfig):
    name = "nublado_bot"

    def ready(self):
        from django_telegram.policies import GroupOnly, PrivateOnly
        from .handlers.misc import start, hello
        from .handlers.group_settings import set_bot_language
        from .handlers.group_points import give_points, POINT_FILTER
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
                with_policies(GroupOnly())(with_language(hello)),
            )
        )

        app.add_handler(
            CommandHandler(
                "set_bot_language",
                with_policies(GroupOnly())(with_language(set_bot_language)),
            )
        )

        app.add_handler(
            MessageHandler(
                POINT_FILTER,
                with_language(give_points),
            )
        )
