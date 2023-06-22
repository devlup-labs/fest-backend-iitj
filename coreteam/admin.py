from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import CoreMember, Vertical


@admin.register(Vertical)
class VerticalAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'rank')
    list_filter = ('name',)
    search_fields = ['name',]
    ordering = ('rank',)

    class Meta:
        model = Vertical
        fields = '__all__'


@admin.register(CoreMember)
class CoreMemberAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'position', 'email')
    list_filter = ('position',)
    search_fields = ['name', 'email', 'phone', 'position']
    ordering = ('position',)

    class Meta:
        model = CoreMember
        fields = '__all__'
