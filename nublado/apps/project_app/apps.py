import logging

from django.apps import AppConfig

logger = logging.getLogger("django")


class ProjectAppConfig(AppConfig):
    name = "project_app"
