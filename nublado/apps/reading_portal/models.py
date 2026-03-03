from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from django_nublado_core.models import TimestampModel, ValidatedSaveModel, LanguageModel
from django_telegram import TelegramUser, TelegramChat, TelegramGroupMember


class ReadingPortal(TimestampModel, ValidatedSaveModel):
    """
    Represents a single Reading Portal session.

    A Reading Portal session has:
      - An English and Spanish text.
      - Scheduling capabilities with opening and closing timestamps.
      - A portal status to check its current state (e.g., open, closed, scheduled).
    """

    class PortalStatus(models.TextChoices):
        SCHEDULED = "scheduled", _("Scheduled")
        OPEN = "open", _("Open")
        CLOSED = "closed", _("Closed")

    title = models.CharField(max_length=200)

    # Reading texts,
    text_en = models.TextField()
    text_es = models.TextField()

    # Lifecycle.
    opens_at = models.DateTimeField()
    closes_at = models.DateTimeField()
    portal_status = models.CharField(
        max_length=20,
        choices=PortalStatus,
        default=PortalStatus.SCHEDULED,
    )
    chat = models.ForeignKey(
        TelegramChat,
        on_delete=models.CASCADE,
        related_name="reading_portals"
    )

    class Meta:
        ordering = ["-opens_at"]

    def __str__(self):
        return f"Reading Portal: {self.title}"

    def clean(self):
        # Only one Reading Portal session may be open at a time.
        if self.portal_status == self.PortalStatus.OPEN:
            existing_open = ReadingSession.objects.filter(status=self.PortalStatus.OPEN)

            if self.pk:
                existing_open = existing_open.exclude(pk=self.pk)

            if existing_open.exists():
                # TODO: Redirect user to the curreently opened Reading Portal.
                raise ValidationError(
                    "There is already an open Reading Portal."
                )

        # The opens_at timestamp must be before the closes_at timestamp.
        if self.opens_at >= self.closes_at:
            raise ValidationError(
                "opens_at must be earlier than closes_at."
            )

    @property
    def is_open(self):
        now = timezone.now()
        return self.opens_at <= now <= self.closes_at

    @classmethod
    def get_current_portal(cls, portal_id=None):
        """
        Return specific portal if portal_id is provided.
        Otherwise, return the currently open portal if it exists.
        """

        if portal_id:
            try:
                return cls.objects.get(pk=portal_id)
            except cls.DoesNotExist:
                return None

        now = timezone.now()

        return cls.objects.filter(
            portal_status=cls.PortalStatus.OPEN,
            opens_at__lte=now,
            closes_at__gte=now,
        ).first()


    # def _submission_counts(self):
    #     """
    #     Helper: return dict mapping member_id -> distinct language count
    #     for active members in this session.
    #     """
    #     submission_counts = (
    #         self.reading_submissions
    #         .filter(
    #             member__is_active=True,
    #             reading_status__in=self.ReadingSubmission.ReadingStatus.ACTIVE_READING_STATUSES,
    #         )
    #         .values("member")
    #         .annotate(lang_count=Count("language", distinct=True))
    #     )
    #     return {entry["member"]: entry["lang_count"] for entry in submission_counts}


    # def members_incomplete_readings(self):
    #     """
    #     Return readers who have not submitted readings in all required languages
    #     for this Reading Portal session.

    #     Note: This only accounts for active participants in the Reading Portal who have submitted
    #     at least one reading.
    #     """

    #     required_count = len(ReadingSubmission.LanguageChoices)
    #     counts = self._submission_counts()

    #     partial_ids = [
    #         member_id
    #         for member_id, lang_count in counts.items()
    #         if 0 < lang_count < required_count
    #     ]
    #     return TelegramGroupMember.objects.filter(id__in=partial_ids)


    def members_incomplete_readings(self):
        """
        Return member readers who submitted at least one reading but not in all languages.
        """
        required_count = len(ReadingSubmission.LanguageChoices)

        members = TelegramGroupMember.objects.filter(
            chat=self.chat,
            is_active=True,
            reading_sessions__reading_portal=self
        ).annotate(
            submitted_count=Count(
                "reading_submissions",
                filter=Q(reading_submissions__reading_portal=self),
            )
        ).filter(submitted_count__lt=required_count, submitted_count__gt=0)

        return members

    def members_complete_readings(self):
        """
        Return readers who have submitted all required readings
        for this Reading Portal session.
        """
        required_count = len(ReadingSubmission.LanguageChoices)

        members = TelegramGroupMember.objects.filter(
            chat=self.chat,
            is_active=True,
            # Only consider members who have at least one submission in this portal.
            reading_submissions__reading_portal=self
        ).annotate(
            submitted_count=Count(
                "reading_submissions",
                # Only count submissions that belong to this session.
                filter=Q(reading_submissions__reading_portal=self),
            )
        ).filter(submitted_count=required_count)

        return members

    def non_participants(self):
        """
        Return active members who haven't submitted any readings for this Reading Portal session.
        """
        members = TelegramGroupMember.objects.filter(
            chat=self.chat,
            is_active=True
        ).exclude(
            readings__session=self
        )

        return members

    # Queue helpers
    def pending_queue_for_language(self, language: str):
        """
        Return pending submissions for the given language, ordered by submission time.
        """
        return self.reading_submissions.filter(
            language=language,
            status=ReadingSubmission.ReadingStatus.PENDING,
            member__is_active=True
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


class ReadingSubmission(LanguageModel):
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
                # TODO: Use ReadingStatus.PENDING in there somehow
                # instead of hardcoded "pending" value.
                condition=models.Q(reading_status="pending"),
                name="unique_pending_submission_per_lang_per_portal",
            )
        ]

    def __str__(self):
        return f"{self.member.user} submission ({self.language}) for {self.reading_portal.title}"
