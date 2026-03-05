from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile, UserSettings


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_verified', 'is_active', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'is_verified', 'date_joined']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone', 'birth_date', 'bio', 'website', 'location')}),
        (_('Avatar'), {'fields': ('avatar',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Login Info'), {'fields': ('last_login_ip',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'theme', 'language', 'timezone', 'created_at']
    list_filter = ['theme', 'language', 'timezone']
    search_fields = ['user__email', 'user__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'privacy_show_email', 'privacy_show_phone', 'marketing_emails', 'newsletter_subscription']
    list_filter = ['privacy_show_email', 'privacy_show_phone', 'marketing_emails', 'newsletter_subscription']
    search_fields = ['user__email', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
