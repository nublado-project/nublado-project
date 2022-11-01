from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import GroupNote


class GroupNoteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass
        
admin.site.register(GroupNote, GroupNoteAdmin)  