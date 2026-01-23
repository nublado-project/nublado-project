import httpx

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from django_telegram.apps import DjangoTelegramConfig
from core.utils import remove_lead_and_trail_slash


from telegram import Bot
import asyncio

webhook_url = "https://nubladoproject.onrender.com/bot/webhook/"
async def set_webhook():
    bot = Bot(settings.DJANGO_TELEGRAM_BOT_TOKEN)
    await bot.set_webhook(
        url=webhook_url,
        secret_token=settings.DJANGO_TELEGRAM_WEBHOOK_SECRET
    )


class Command(BaseCommand):
    help = "Sets bots webhooks asynchronously after they have been initialized."

    def handle(self, *args, **options):
        asyncio.run(set_webhook())


        self.stdout.write(
            self.style.SUCCESS(f"Webhook successfully set to {webhook_url}")
        )

        return
