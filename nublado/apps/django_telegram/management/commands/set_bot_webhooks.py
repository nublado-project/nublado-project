import asyncio

from telegram import Bot

from django.core.management.base import BaseCommand
from django.conf import settings

BOTS = settings.BOTS


class Command(BaseCommand):
    def handle(self, *args, **options):
        asyncio.run(self.run())

    async def run(self):
        for bot_name, (bot_token, webhook_url, webhook_token) in BOTS.items():
            bot = Bot(bot_token)
            await bot.set_webhook(
                url=webhook_url, secret_token=webhook_token, drop_pending_updates=True
            )

            self.stdout.write(self.style.SUCCESS(f"{bot_name} webhook set"))
