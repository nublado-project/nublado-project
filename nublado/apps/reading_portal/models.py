from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django_nublado_core.models import TimestampModel, ValidatedSaveModel, LanguageModel
from django_telegram.models import TelegramChat, TelegramGroupMember

from .managers import ReadingPortalManager


class ReadingPortal(TimestampModel):
    """
    A Reading Portal session.
    """

    REQUIRED_LANGUAGES = {"en", "es"}

    class PortalStatus(models.TextChoices):
        DRAFT = "draft", _("Draft")
        SCHEDULED = "scheduled", _("Scheduled")
        OPEN = "open", _("Open")
        CLOSED = "closed", _("Closed")

    chat = models.ForeignKey(
        TelegramChat, on_delete=models.CASCADE, related_name="reading_portals"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(
        blank=True,
        help_text="Optional description shown in the portal intro message."
    )
    pinned_message_id = models.BigIntegerField(
        null=True,
        blank=True,
        help_text="Telegram message id of the pinned portal intro message."
    )
    portal_status = models.CharField(
        max_length=20,
        choices=PortalStatus,
        default=PortalStatus.DRAFT,
    )
    max_mistakes = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Maximum number of corrections per submission."
    )

    # Lifecycle.
    opens_at = models.DateTimeField(null=True, blank=True)
    closes_at = models.DateTimeField(null=True, blank=True)

    objects = ReadingPortalManager()

    class Meta:
        ordering = ["-date_created"]

        models.UniqueConstraint(
            fields=["chat"],
            condition=Q(portal_status="open"),
            name="only_one_open_portal_per_chat"
        )

    def __str__(self):
        return f"Reading Portal: {self.title}"

    def clean(self):
        # Only one Reading Portal session may be open at a time.
        if self.portal_status == self.PortalStatus.OPEN:
            existing_open = ReadingPortal.objects.filter(
                chat=self.chat, portal_status=self.PortalStatus.OPEN
            )
            if self.pk:
                existing_open = existing_open.exclude(pk=self.pk)

            if existing_open.exists():
                # TODO: Redirect user to the curreently opened Reading Portal.
                raise ValidationError("There is already an open Reading Portal.")

        # The opens_at timestamp must be before the closes_at timestamp.
        if self.opens_at and self.closes_at:
            if self.opens_at >= self.closes_at:
                raise ValidationError("opens_at must be earlier than closes_at.")

    @property
    def is_open(self):
        now = timezone.now()

        if not self.opens_at or not self.closes_at:
            return False

        return (
            self.portal_status == self.PortalStatus.OPEN
            and self.opens_at <= now <= self.closes_at
        )

    async def open_portal(self):
        if not await self.ahas_required_languages():
            raise ValidationError(
                "Portal must have exactly English and Spanish readings."
            )

        self.portal_status = self.PortalStatus.OPEN
        await self.asave(update_fields=["portal_status"])

    async def ahas_required_languages(self):
        existing = {
            lang async for lang in
            self.portal_readings.values_list("language", flat=True)
        }

        return existing == self.REQUIRED_LANGUAGES

    def members_incomplete_readings(self):
        """
        Return member readers who submitted at least one reading but not in all languages
        for this Reading Portal session.
        """
        required_count = len(self.REQUIRED_LANGUAGES)

        members = (
            TelegramGroupMember.objects.filter(
                chat=self.chat, is_active=True, reading_sessions__reading_portal=self
            )
            .annotate(
                submitted_count=Count(
                    "reading_submissions",
                    filter=Q(reading_submissions__reading_portal=self),
                )
            )
            .filter(submitted_count__lt=required_count, submitted_count__gt=0)
        )

        return members

    def members_complete_readings(self):
        """
        Return member readers who have submitted all required readings
        for this Reading Portal session.
        """
        required_count = len(self.REQUIRED_LANGUAGES)

        members = (
            TelegramGroupMember.objects.filter(
                chat=self.chat,
                is_active=True,
                # Only consider members who have at least one submission in this portal.
                reading_submissions__reading_portal=self,
            )
            .annotate(
                submitted_count=Count(
                    "reading_submissions",
                    # Only count submissions that belong to this session.
                    filter=Q(reading_submissions__reading_portal=self),
                )
            )
            .filter(submitted_count=required_count)
        )

        return members

    def non_participants(self):
        """
        Return active members who haven't submitted any readings for this Reading Portal session.
        """
        members = TelegramGroupMember.objects.filter(
            chat=self.chat, is_active=True
        ).exclude(reading_submissions__reading_portal=self)

        return members

    # Queue helpers
    def pending_queue_for_language(self, language: str):
        """
        Return pending submissions for the given language, ordered by submission time.
        """
        return self.reading_submissions.filter(
            language=language,
            status=ReadingSubmission.ReadingStatus.PENDING,
            member__is_active=True,
        ).order_by("submitted_at")

    def next_submission(self, language: str):
        """
        Peek at the next pending submission in the queue for a language.
        """
        return self.pending_queue_for_language(language).first()

    # def resubmit(self, submission: ReadingSubmission):
    #     """
    #     Handle resubmission:
    #     - Remove old submission
    #     - Member goes to the end of the queue
    #     """
    #     submission.delete()


class PortalReading(TimestampModel, LanguageModel):
    """
    A language-specific reading provided by a ReadingPortal.
    """

    reading_portal = models.ForeignKey(
        ReadingPortal, related_name="portal_readings", on_delete=models.CASCADE
    )
    message_id = models.BigIntegerField(null=True, blank=True)
    message_text = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["reading_portal", "language"], name="unique_language_per_portal"
            )
        ]

    def clean(self):
        if not self.message_id and not self.message_text:
            raise ValidationError(
                "Either message_id or message_text must be provided."
            )


class ReadingSubmission(TimestampModel, LanguageModel):
    """
    A reading submission for a Reading Portal session.
    """

    # Note: Superseded status = "This reading is old and doesn't count.
    # A newer version has been submitted that supersedes this one."
    class ReadingStatus(models.TextChoices):
        PENDING = "pending", _("Pending")
        REVIEWED = "reviewed", _("Reviewed")
        SUPERSEDED = "superseded", _("Superseded")

    ACTIVE_READING_STATUSES = [ReadingStatus.PENDING, ReadingStatus.REVIEWED]

    reading_portal = models.ForeignKey(
        ReadingPortal,
        on_delete=models.CASCADE,
        related_name="reading_submissions",
    )
    member = models.ForeignKey(
        TelegramGroupMember,
        on_delete=models.CASCADE,
        related_name="reading_submissions",
    )

    # Telegram message id of the reading.
    reading_message_id = models.BigIntegerField()
    reading_status = models.CharField(
        max_length=40,
        choices=ReadingStatus,
        default=ReadingStatus.PENDING,
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["submitted_at"]
        # Only one pendng reading submission per user per language.
        # Superseded (resubmitted) reading submissions are the exception.
        constraints = [
            models.UniqueConstraint(
                fields=["reading_portal", "member", "language"],
                condition=models.Q(reading_status="pending"),
                name="unique_pending_submission_per_lang_per_portal",
            )
        ]

    def __str__(self):
        return f"{self.member.user} submission ({self.language}) for {self.reading_portal.title}"
