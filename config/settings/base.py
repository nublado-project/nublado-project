import os
import sys
import datetime as dt
from pathlib import Path

from django.utils.translation import gettext_noop as _


# Get key env values from the virtual environment.
def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable.".format(var_name)
        raise Exception(error_msg)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Custom directory for apps
APP_DIR = "nublado/apps"
sys.path.append(os.path.join(BASE_DIR, APP_DIR))

APPS_ROOT = BASE_DIR / APP_DIR

PROJECT_NAME = "Nublado Project"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = []

# Installed apps
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
LOCAL_APPS = [
    "core.apps.CoreConfig",
    "users.apps.UserConfig",
    # "django_telegram.apps.DjangoTelegramConfig",
    "bot_registry.apps.BotRegistryConfig",
    "nublado_bot.apps.NubladoBotConfig",
    "project_app.apps.ProjectAppConfig",
]
THIRD_PARTY_APPS = [
    "import_export",
]
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

AUTH_USER_MODEL = "users.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "project_app.context_processors.global_settings",
            ],
        },
    },
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization and localization
EN = "en"
ES = "es"
LANGUAGE_CODE = EN
LANGUAGES = [
    (EN, _("common.language.en")),
    (ES, _("common.language.es")),
]
LANGUAGES_DICT = dict(LANGUAGES)

LOCALE_PATHS = (APPS_ROOT / "project_app" / "locale",)

TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / APP_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Logging
LOGGING = {
    "version": 1,
    # Version of logging
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    # Handlers
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "nublado-debug.log",
        },
        "console": {
            "level": "INFO",
            # 'filters': ['require_debug_true'],
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    # Loggers
    "loggers": {
        "django": {
            "handlers": ["console"],
            "propagate": True,
        },
        "django-debug": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

MON, TUE, WED, THU, FRI, SAT, SUN = range(7)
WEEKDAYS = [
    _("common.monday"),
    _("common.tuesday"),
    _("common.wednesday"),
    _("common.thursday"),
    _("common.friday"),
    _("common.saturday"),
    _("sommon.sunday"),
]
WEEKDAYS_ABBR = [
    _("common.abbr.monday"),
    _("common.abbr.tuesday"),
    _("common.abbr.wednesday"),
    _("common.abbr.thursday"),
    _("common.abbr.friday"),
    _("common.abbr.saturday"),
    _("common.abbr.sunday"),
]

# Telegram bot stuff
BOT_MODE_WEBHOOK = "webhook"
BOT_MODE_POLLING = "polling"

NUBLADO_BOT = "nublado_bot"
NUBLADO_BOT_TOKEN = get_env_variable("NUBLADO_BOT_TOKEN")
NUBLADO_BOT_WEBHOOK_URL = "https://nubladoproject.onrender.com/bot/nublado/webhook/"
NUBLADO_BOT_WEBHOOK_SECRET = "supersecretnubladowebhooktoken"

DJANGO_TELEGRAM_BOT_TOKEN = NUBLADO_BOT_TOKEN
DJANGO_TELEGRAM_WEBHOOK_URL = "https://nubladoproject.onrender.com/bot/webhook/"
DJANGO_TELEGRAM_WEBHOOK_SECRET = "supersecretwebhooktoken"

BOTS = {
    NUBLADO_BOT: (
        NUBLADO_BOT_TOKEN, 
        NUBLADO_BOT_WEBHOOK_URL,
        NUBLADO_BOT_WEBHOOK_SECRET
    ),
}
