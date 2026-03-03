import logging

logger = logging.getLogger("django")


# def with_language(callback):
#     @wraps(callback)
#     async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE):
#         language_resolver = context.application.bot_data.get("language_resolver")

#         if language_resolver is None:
#             set_context_language(context, settings.LANGUAGE_CODE)
#         else:
#             # Resolve the language.
#             try:
#                 await language_resolver(update, context)
#             except Exception as e:
#                 logger.exception("Error resolving chat language.")
#                 set_context_language(context, settings.LANGUAGE_CODE)

#         return await callback(update, context)

#     return wrapped
