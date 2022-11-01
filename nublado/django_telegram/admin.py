from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import GroupMember


class GroupMemberAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass
        
admin.site.register(GroupMember, GroupMemberAdmin)  