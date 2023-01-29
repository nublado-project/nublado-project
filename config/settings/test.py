from .base import *

TESTING = True
DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ["TEST_DATABASE_NAME"],
        "USER": os.environ["DATABASE_USER"],
        "PASSWORD": os.environ["DATABASE_PWD"],
        "HOST": "localhost",
        "PORT": "",
        "TEST": {
            "NAME": os.environ["TEST_DATABASE_NAME"],
        }
    }
}

DJANGO_TELEGRAM['mode'] = BOT_MODE_POLLING
DJANGO_TELEGRAM['bots'][TEST_BOT_TOKEN] = {
    'token': TEST_BOT_TOKEN,
    'group_id': TEST_GROUP_ID,
    'repo_id': TEST_REPO_ID,
    'sudo_list': TEST_SUDO_LIST
}

DJANGO_TELEGRAM['testing'] = {
    'api_id': get_env_variable('TG_API_KEY'),
    'api_hash': get_env_variable('TG_API_HASH'),
    'api_session_str': get_env_variable('TG_API_SESSION_STR')
}

BOT_CLI[TEST_BOT] = DJANGO_TELEGRAM['bots'][TEST_BOT_TOKEN]
