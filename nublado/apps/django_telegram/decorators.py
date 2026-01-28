from functools import wraps

from telegram import Update
from telegram.ext import ApplicationHandlerStop, ContextTypes

from django.utils.translation import activate, get_language


def with_language(callback):
    @wraps(callback)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE):
        language_resolver = context.application.bot_data.get("language_resolver")
        old_language = get_language() or settings.LANGUAGE_CODE

        try:
            # Activate language.
            if language_resolver:
                language_code = await language_resolver(update, context)
                activate(language_code)
            return await callback(update, context)
        finally:
            activate(old_language)

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