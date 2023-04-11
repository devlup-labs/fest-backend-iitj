from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *


@admin.register(Verticles)
class VerticlesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'rank')
    list_filter = ('name',)
    search_fields = ['name', 'rank']
    ordering = ('rank',)

    class Meta:
        model = Verticles
        fields = '__all__'


@admin.register(CoreTeam)
class CoreTeamAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'position', 'email')
    list_filter = ('position',)
    search_fields = ['name', 'email', 'phone', 'position']
    ordering = ('position',)

    class Meta:
        model = CoreTeam
        fields = '__all__'
