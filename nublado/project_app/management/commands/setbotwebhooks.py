import httpx

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from django_telegram.apps import DjangoTelegramConfig
from core.utils import remove_lead_and_trail_slash


class Command(BaseCommand):
    help = "Sets bots webhooks asynchronously after they have been initialized."

    def handle(self, *args, **options):
        dt = settings.DJANGO_TELEGRAM
        bots = dt['bots']
        webhook_site = remove_lead_and_trail_slash(dt['webhook_site'])
        set_webhook_path = remove_lead_and_trail_slash(dt['set_webhook_path'])

        for bot_id, bot_conf in bots.items():
            set_webhook_url = f"{webhook_site}/{set_webhook_path}/{bot_conf['name']}/"
            r = httpx.post(set_webhook_url, data={})
            if r.status_code == httpx.codes.OK:
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully set webhook for {bot_conf['name']} from command.")
                )
            else:
                raise CommandError(f"Error setting webhook for {bot_conf['name']} from command. {r}")

        return