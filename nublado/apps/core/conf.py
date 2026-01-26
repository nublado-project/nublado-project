from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from django.conf import settings as django_settings


"""
Simple, prefix-based app settings.

Thanks to a blog post by Benjamin Balder Back for the idea.
https://overtag.dk/v2/blog/a-settings-pattern-for-reusable-django-apps/
"""


@dataclass(frozen=True)
class AppSettingsBase(ABC):

    def __init__(self, *args, **kwargs):
        # Raise an error if app_settings_prefix isn't implemented as a property.
        attr = getattr(type(self), "app_settings_prefix", None)
        if not isinstance(attr, property):
            raise TypeError("The method app_settings_prefix must be implemented as a property.")

    def __getattribute__(self, __name: str) -> Any:
        """
        Get prefixed attribute from app settings, or prefixed attribute from django.conf.settings.

        Note: To avoid a recursive mess, if referring to an attribute in this method, 
        use object.__getattribute__(self, "attr_name")
        """
        if __name.startswith(object.__getattribute__(self, "app_settings_prefix")) and hasattr(django_settings, __name):
            return getattr(django_settings, __name)

        return super().__getattribute__(__name)

    @property
    @abstractmethod
    def app_settings_prefix(self):
        """
        The app settings prefix is required (e.g., "MY_APP_").

        Note: The subclass that implements this method must implement it 
        as a property.
        """
        pass
