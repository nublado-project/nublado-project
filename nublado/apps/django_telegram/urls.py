from django.conf import settings
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import telegram_webhook

app_name = "django_telegram"

urlpatterns = [
    path("webhook/", telegram_webhook),
]

# urlpatterns = [
#     re_path(
#         r"^setwebhook/(?P<bot_id>.+)/$",
#         csrf_exempt(BotSetWebhookView.as_view()),
#         name="bot_set_webhook_view",
#     ),
#     re_path(
#         r"^webhook/(?P<bot_id>.+)/$",
#         csrf_exempt(BotWebhookView.as_view()),
#         name="bot_webhook_view",
#     ),
# ]
