import uuid

from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class ValidatedSaveModel(models.Model):
    """
    An abstract model that's just a quick "workaround" to validate a subclassed model instance
    before saving it, without overriding the model's save method and inadvertently
    messing something up.
    """

    class Meta:
        abstract = True

    def validate_and_save(self):
        self.full_clean()
        self.save()


class TimestampModel(models.Model):
    """
    An abstract model that keeps track of when a subclassed model
    instance has been created and updated.
    """

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """
    An abstract model that generates a uuid for a subclassed
    model's id (primary key) field.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


LanguageChoices = settings.LANGUAGES_ENUM


class LanguageModel(models.Model):
    """
    An abstract model that provides a language choices
    field populated by the project's language settings.
    """

    LanguageChoices = LanguageChoices

    language = models.CharField(
        max_length=2,
        choices=LanguageChoices,
        default=LanguageChoices.EN,
    )

    class Meta:
        abstract = True
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_language_valid",
                # Can't refer to LanguageChoices in model.
                condition=models.Q(language__in=LanguageChoices.values),
            )
        ]


class PublishedModel(models.Model):
    """
    An abstract model for "publishable" for models
    (e.g., blog posts, news articles).
    """

    class PublishedStatus(models.TextChoices):
        DRAFT = ("DRAFT", _("Draft"))
        PUBLISHED = ("PUBLISHED", _("Published"))

    published_status = models.CharField(
        max_length=20,
        choices=PublishedStatus,
        default=PublishedStatus.DRAFT,
    )
    date_published = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    @property
    def is_published(self):
        return self.published_status == self.PublishedStatus.PUBLISHED

    def publish(self):
        """
        Set published status to published and save.
        """
        self.published_status = self.PublishedStatus.PUBLISHED
        self.full_clean()
        self.save()

    def unpublish(self):
        """
        Set published status to draft and save.
        """
        self.published_status = self.PublishedStatus.DRAFT
        self.full_clean()
        self.save()
