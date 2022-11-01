from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import GroupMemberPoints


class GroupMemberPointsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass
        
admin.site.register(GroupMemberPoints, GroupMemberPointsAdmin)  