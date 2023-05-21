import logging

import httpx

from django.apps import AppConfig
from django.conf import settings

from core.utils import remove_lead_and_trail_slash

logger = logging.getLogger('django')


class ProjectAppConfig(AppConfig):
    name = "project_app"

    def setup_bots(self):
        dt = settings.DJANGO_TELEGRAM
        if dt['mode'] == settings.BOT_MODE_WEBHOOK:
            from django_telegram.apps import DjangoTelegramConfig

            for bot_name, conf in settings.DJANGO_TELEGRAM['bots'].items():
                try:
                    bot_token = conf['token']
                    bot = DjangoTelegramConfig.bot_registry.get_bot(bot_token)
                    if bot:
                        set_webhook_site = remove_lead_and_trail_slash(dt['webhook_site'])
                        set_webhook_path = remove_lead_and_trail_slash(dt['set_webhook_path'])
                        set_webhook_url = f"{set_webhook_site}/{set_webhook_path}/{bot.token}/"
                        logger.info(set_webhook_url)
                        r = httpx.post(set_webhook_url, data={})
                        if r.status_code != httpx.codes.OK:
                            logger.error(f"Error starting bot {bot.token} webhook with post request.")
                    else:
                        logger.error(f"Bot {bot_name} doesn't exist or is improperly configured.")
                except Exception as e:
                    logger.error(f"Bot {bot_name} doesn't exist or is improperly configured.")
                    logger.error(e)
    def ready(self):
        self.setup_bots()