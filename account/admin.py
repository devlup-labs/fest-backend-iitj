from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *


@admin.register(UserProfile)
class UserProfileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('email', 'contact', 'college')
    list_filter = ('college',)
    search_fields = ['email', 'college', 'contact', 'city']
    ordering = ('email',)

    class Meta:
        model = UserProfile
        fields = '__all__'

