from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin


from .models import UserProfile, User
# I want to register my Abstrated user model User in admin

class UserProfileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'contact', 'college')
    list_filter = ('college',)
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