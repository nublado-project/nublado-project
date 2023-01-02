import logging

from django.conf import settings
from django.apps import AppConfig

logger = logging.getLogger('django')


class GroupNotesConfig(AppConfig):
    name = "group_notes"