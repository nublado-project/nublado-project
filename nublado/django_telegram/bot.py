import logging

from core.utils import remove_lead_and_trail_slash
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Defaults, ExtBot as TelegramBot,
    CommandHandler, Application, ApplicationBuilder
)

from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger('django')

BOT_MODE_ERROR = "Bot mode must be polling or webhooks."


class Bot(object):
    def __init__(
        self,
        token: str,
        name: str = None,
        webhook_url: str = None
    ):
        self.token = token
        self.name = name
        defaults = Defaults(parse_mode=ParseMode.MARKDOWN)
        self.telegram_bot = TelegramBot(
            self.token,
            defaults=defaults
        )
        self.application = None
        self.webhook_url = webhook_url

        try:
            dt = settings.DJANGO_TELEGRAM
            if dt['mode'] == settings.BOT_MODE_POLLING:
                self.application = ApplicationBuilder().bot(self.telegram_bot).build()
            elif dt['mode'] == settings.BOT_MODE_WEBHOOK:
                self.application = Application.builder().bot(self.telegram_bot).updater(None).build()
                if not webhook_url:
                    webhook_site = remove_lead_and_trail_slash(dt['webhook_site'])
                    webhook_path = remove_lead_and_trail_slash(dt['webhook_path'])
                    self.webhook_url = f"{webhook_site}/{webhook_path}/{self.name}/"
            else:
                raise ImproperlyConfigured(BOT_MODE_ERROR)
        except Exception as e:
            logger.error(e)

    def start_polling(self):
        logger.info("Bot mode: polling")
        self.application.run_polling()

    async def set_webhook(self):
        if self.webhook_url:
            await self.telegram_bot.set_webhook(
                self.webhook_url,
                allowed_updates=Update.ALL_TYPES
            )
            logger.info(f"Bot {self.name} webhook set.")
        else:
            logger.error(f"Bot {self.name} webhook url isn't set.")
            raise ImproperlyConfigured()

    def add_handler(self, handler, handler_group: int = 0):
        try:
            self.application.add_handler(handler, group=handler_group)
        except:
            logger.error(f"Error adding handler {handler}")

    def remove_handler(self, handler, handler_group:int = 0):
        try:
            self.application.remove_handler(handler, group=handler_group)
        except:
            logger.error(f"Error removing handler {handler}")

    def add_command_handler(self, command: str, func, handler_group: int = 0):
        handler = CommandHandler(command, func)
        self.add_handler(handler, handler_group)