from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from django.contrib.auth.admin import UserAdmin


from .models import UserProfile, User, BlacklistedEmail, PreRegistration


class BlacklistedEmailAdmin(admin.ModelAdmin):
    class Meta:
        model = BlacklistedEmail


admin.site.register(BlacklistedEmail, BlacklistedEmailAdmin)


class PreRegistrationAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('full_name', 'email', 'contact', 'college', 'current_year', 'city')
    list_filter = ('college', 'current_year', 'city')

    class Meta:
        model = PreRegistration


admin.site.register(PreRegistration, PreRegistrationAdmin)


class UserProfileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'contact', 'college', 'registration_code')
    list_filter = ('college', 'amount_paid')
    search_fields = ['user', 'college', 'contact', 'city']
    ordering = ('college',)

    class Meta:
        model = UserProfile
        fields = '__all__'


admin.site.register(UserProfile, UserProfileAdmin)


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'profile_complete')
    list_filter = ('email', 'username', 'profile_complete')
    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username', 'profile_complete')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2', 'username', 'profile_complete')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )


admin.site.register(User, CustomUserAdmin)
