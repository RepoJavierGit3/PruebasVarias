from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel


class User(AbstractUser):
    """
    Custom user model with additional fields
    """
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone'), max_length=20, blank=True)
    avatar = models.ImageField(_('avatar'), upload_to='avatars/', blank=True)
    birth_date = models.DateField(_('birth date'), null=True, blank=True)
    bio = models.TextField(_('bio'), max_length=500, blank=True)
    website = models.URLField(_('website'), blank=True)
    location = models.CharField(_('location'), max_length=100, blank=True)
    is_verified = models.BooleanField(_('verified'), default=False)
    last_login_ip = models.GenericIPAddressField(_('last login IP'), null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return f"https://ui-avatars.com/api/?name={self.full_name}&background=random"


class UserProfile(BaseModel):
    """
    Extended user profile with additional settings
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    theme = models.CharField(max_length=20, default='light', choices=[
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('auto', 'Auto'),
    ])
    language = models.CharField(max_length=10, default='es', choices=[
        ('es', 'Spanish'),
        ('en', 'English'),
    ])
    timezone = models.CharField(max_length=50, default='America/Mexico_City')

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')

    def __str__(self):
        return f"{self.user.email} Profile"


class UserSettings(BaseModel):
    """
    User-specific settings and preferences
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    privacy_show_email = models.BooleanField(default=False)
    privacy_show_phone = models.BooleanField(default=False)
    privacy_show_location = models.BooleanField(default=True)
    marketing_emails = models.BooleanField(default=False)
    newsletter_subscription = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('User Settings')
        verbose_name_plural = _('User Settings')

    def __str__(self):
        return f"{self.user.email} Settings"
