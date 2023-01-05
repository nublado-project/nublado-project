import os
import sys
import datetime as dt
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_noop as _


# Get key env values from the virtual environment.
def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable.".format(var_name)
        raise ImproperlyConfigured(error_msg)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Subdirectory for app bundles.
APP_DIR = 'nublado'
sys.path.append(os.path.join(BASE_DIR, APP_DIR))

APPS_ROOT = BASE_DIR / APP_DIR

PROJECT_NAME = "Nublado Project"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = []

# Installed apps
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
LOCAL_APPS = [
    'core.apps.CoreConfig',
    'users.apps.UserConfig',
    'django_telegram.apps.DjangoTelegramConfig',
    'bot_misc.apps.BotMiscConfig',
    'group_admin.apps.GroupAdminConfig',
    'group_notes.apps.GroupNotesConfig',
    'group_points.apps.GroupPointsConfig',
    'nublado_bot.apps.NubladoBotConfig',
    'proto_bot.apps.ProtoBotConfig',
    'project_app.apps.ProjectAppConfig'
]
THIRD_PARTY_APPS = [
    'import_export',
]
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware'
]

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'project_app.context_processors.global_settings'
            ],
        },
    },
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization and localization
EN = 'en'
ES = 'es'
FREE = 'free'
LANGUAGE_CODE = EN
LANGUAGES = [
    (EN, _("English")),
    (ES, _("Spanish")),
]
LANGUAGES_DICT = dict(LANGUAGES)

LOCALE_PATHS = (
    APPS_ROOT / "project_app" / "locale",
)

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / APP_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging
LOGGING = {
    'version': 1,
    # Version of logging
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # Handlers
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'nublado-debug.log',
        },
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    # Loggers
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
    },
}

MON, TUE, WED, THU, FRI, SAT, SUN = range(7)
# LANGUAGE_DAYS = {
#     EN: _("English"),
#     ES: _("Spanish"),
#     FREE: _("Free")
# }
# LANGUAGE_DAY_HOUR_CHANGE = 0
# LANGUAGE_DAY_MINUTE_CHANGE = 1
# LANGUAGE_DAY_TIME_CHANGE = dt.time(
#     hour=LANGUAGE_DAY_HOUR_CHANGE,
#     minute=LANGUAGE_DAY_MINUTE_CHANGE
# ).strftime('%H:%M')
WEEKDAYS = [
    _("Monday"), _("Tuesday"), _("Wednesday"), _("Thursday"),
    _("Friday"), _("Saturday"), _("Sunday")
]
WEEKDAYS_ABBR = [
    _("Mon."), _("Tue."), _("Wed."), _("Thu."),
    _("Fri."), _("Sat."), _("Sun.")
]

# Telegram bot stuff
BOT_MODE_WEBHOOK = "webhook"
BOT_MODE_POLLING = "polling"

#NubladoBot
# Command line arg to run this bot
NUBLADO_BOT = 'nubladobot'
NUBLADO_BOT_TOKEN = get_env_variable('NUBLADO_BOT_TOKEN')
NUBLADO_GROUP_ID = int(get_env_variable('NUBLADO_GROUP_ID'))
NUBLADO_REPO_ID = int(get_env_variable('NUBLADO_REPO_ID'))
NUBLADO_GROUP_OWNER_ID = int(get_env_variable('NUBLADO_GROUP_OWNER_ID'))
NUBLADO_SUDO_LIST = [
    NUBLADO_GROUP_OWNER_ID,
]

# Command line arg to run this bot
PROTO_BOT = 'protobot'
PROTO_BOT_TOKEN = get_env_variable('PROTO_BOT_TOKEN')
PROTO_GROUP_ID = int(get_env_variable('PROTO_GROUP_ID'))
PROTO_GROUP_2_ID = int(get_env_variable('PROTO_GROUP_2_ID'))

PROTO_REPO_ID = NUBLADO_REPO_ID
PROTO_GROUP_OWNER_ID = NUBLADO_GROUP_OWNER_ID
PROTO_SUDO_LIST = [
    PROTO_GROUP_OWNER_ID, 
]

DJANGO_TELEGRAM = {
    'mode': BOT_MODE_WEBHOOK,
    'webhook_port': int(os.environ.get('PORT', 5000)),
    'webhook_site' : "https://nubladoproject.onrender.com",
	'webhook_path' : "bot/webhook",
    'bots': {
        NUBLADO_BOT_TOKEN: {
            'token': NUBLADO_BOT_TOKEN,
            'group_id': NUBLADO_GROUP_ID,
            'repo_id': NUBLADO_REPO_ID,
            'sudo_list': NUBLADO_SUDO_LIST
        },
        PROTO_BOT_TOKEN: {
            'token': PROTO_BOT_TOKEN,
            'group_id': PROTO_GROUP_ID,
            'repo_id': PROTO_REPO_ID,
            'sudo_list': PROTO_SUDO_LIST
        },
    }
}

BOT_CLI = {
    NUBLADO_BOT: DJANGO_TELEGRAM['bots'][NUBLADO_BOT_TOKEN],
    PROTO_BOT: DJANGO_TELEGRAM['bots'][PROTO_BOT_TOKEN]
}
