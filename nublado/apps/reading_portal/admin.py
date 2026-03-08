from django.contrib import admin

from .models import ReadingPortal, PortalReading, ReadingSubmission


@admin.register(ReadingPortal)
class ReadingPortalAdmin(admin.ModelAdmin):
    list_display = ("title", "chat", "portal_status", "opens_at", "closes_at")
    list_filter = ("portal_status", "chat")
    search_fields = ("title",)


@admin.register(PortalReading)
class PortalReadingAdmin(admin.ModelAdmin):
    list_display = ("reading_portal", "language", "message_id", "message_text")
    list_filter = ("language", "reading_portal")


@admin.register(ReadingSubmission)
class ReadingSubmissionAdmin(admin.ModelAdmin):
    list_display = ("portal_reading", "message_id")
