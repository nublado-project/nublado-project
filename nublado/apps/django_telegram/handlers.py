from telegram import Update
from telegram.ext import BaseHandler, ContextTypes

from django.conf import settings

from .utils.helpers import set_context_language
from .utils.database import resolve_chat_language


class LanguageHandler(BaseHandler):
    """
    Middleware-style handler that ensures language is resolved
    before any other handler executes.
    """

    def __init__(self):
        super().__init__(callback=None)

    def check_update(self, update: object) -> bool:
        # Run for every update that has a chat
        return isinstance(update, Update) and update.effective_chat is not None

    async def handle_update(
        self,
        update: Update,
        application,
        check_result,
        context: ContextTypes.DEFAULT_TYPE,
    ):
        try:
            await resolve_chat_language(update, context)
        except Exception:
            set_context_language(context, settings.LANGUAGE_CODE)

        # DO NOT stop processing
        return