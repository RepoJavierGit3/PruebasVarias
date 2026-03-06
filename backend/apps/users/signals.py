from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserProfile, UserSettings

User = get_user_model()


# Temporarily commented out for testing
# @receiver(post_save, sender=User)
# def create_user_profile_and_settings(sender, instance, created, **kwargs):
#     """
#     Create user profile and settings when a new user is created
#     """
#     if created:
#         UserProfile.objects.get_or_create(user=instance)
#         UserSettings.objects.get_or_create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile_and_settings(sender, instance, **kwargs):
#     """
#     Save user profile and settings when user is updated
#     """
#     if hasattr(instance, 'profile'):
#         instance.profile.save()
#     if hasattr(instance, 'settings'):
#         instance.settings.save()
