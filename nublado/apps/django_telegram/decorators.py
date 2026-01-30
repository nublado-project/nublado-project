import logging
from functools import wraps

from telegram import Update
from telegram.ext import ApplicationHandlerStop, ContextTypes

from django.conf import settings

from .utils.helpers import set_context_language

logger = logging.getLogger("django")


def with_language(callback):
    @wraps(callback)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE):
        language_resolver = context.application.bot_data.get("language_resolver")

        if language_resolver is None:
            logger.warning(
                "language_resolver not found in application.bot_data. "
                "Falling back to default language"
            )
            set_context_language(context, settings.LANGUAGE_CODE)

        else:
            # Resolve the language.
            try:
                await language_resolver(update, context)
            except Exception as e:
                logger.exception("Error resolving chat language, using default")
                set_context_language(context, settings.LANGUAGE_CODE)

        return await callback(update, context)

    return wrapped


def with_policies(*policies):
    def decorator(callback):
        @wraps(callback)
        async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE):
            # Check policies.
            for policy in policies:
                allowed = await policy.check(update, context)
                if not allowed:
                    raise ApplicationHandlerStop

            # Call original handler.
            return await callback(update, context)

        return wrapped

    return decorator
