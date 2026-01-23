import httpx

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from django_telegram.apps import DjangoTelegramConfig
from core.utils import remove_lead_and_trail_slash

from telegram import Bot
import asyncio


class Command(BaseCommand):
    help = "Sets bots webhooks asynchronously after they have been initialized."

    def handle(self, *args, **options):
        asyncio.run(self.set_webhook())

    async def set_webhook(self):
        bot = Bot(settings.DJANGO_TELEGRAM_BOT_TOKEN)
        webhook_url = settings.DJANGO_TELEGRAM_WEBHOOK_URL
        secret_token = getattr(settings, "DJANGO_TELEGRAM_WEBHOOK_SECRET", None)

        await bot.set_webhook(
            url=webhook_url,
            secret_token=secret_token,
            drop_pending_updates=True,
        )

        self.stdout.write(self.style.SUCCESS(f"Webhook set to {webhook_url}"))
