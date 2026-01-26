from django.contrib import admin

from .models import TelegramUser, TelegramChat


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = [
        "telegram_id",
        "username",
        "first_name",
        "last_name",
        "is_bot",
        "date_created",
        "date_updated",
    ]


@admin.register(TelegramChat)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = [
        "telegram_id",
        "username",
        "title",
        "username",
        "date_created",
        "date_updated",
    ]
