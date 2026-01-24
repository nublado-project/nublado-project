from telegram.ext import filters

# Chat type filters
PRIVATE = filters.ChatType.PRIVATE
GROUPS = filters.ChatType.GROUPS
CHANNEL = filters.ChatType.CHANNEL

# Message filters
TEXT_ONLY = filters.TEXT & ~filters.COMMAND
COMMAND_ONLY = filters.COMMAND
PHOTO_ONLY = filters.PHOTO