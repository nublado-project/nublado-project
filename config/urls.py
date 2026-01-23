from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from nublado_bot.webhook import webhook as nublado_bot_webhook

urlpatterns = [
    path("", include("project_app.urls")),
    path("admin/", admin.site.urls),
    path("bot/nublado/webhook", nublado_bot_webhook)
    # path("bot/", include("django_telegram.urls", namespace="bot")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
