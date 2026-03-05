from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import AuditLog

User = get_user_model()


@receiver(post_save)
def audit_log_save(sender, instance, created, **kwargs):
    """
    Signal to log model creation and updates
    """
    # Skip audit logs for AuditLog model itself to avoid infinite recursion
    if sender == AuditLog:
        return
    
    # Skip during migrations
    from django.core.management.commands import migrate
    import inspect
    if 'migrate' in inspect.stack()[-1].filename:
        return
    
    # Skip certain models that don't need auditing
    skip_models = ['Session', 'LogEntry', 'Migration']
    if sender.__name__ in skip_models:
        return
    
    action = 'CREATE' if created else 'UPDATE'
    
    try:
        AuditLog.objects.create(
            action=action,
            model_name=sender.__name__,
            object_id=instance.id,
            object_repr=str(instance)[:200],
            changes={'instance': instance.__dict__} if not created else {}
        )
    except:
        # Silently fail during migrations or setup
        pass


@receiver(post_delete)
def audit_log_delete(sender, instance, **kwargs):
    """
    Signal to log model deletion
    """
    # Skip audit logs for AuditLog model itself
    if sender == AuditLog:
        return
    
    # Skip during migrations
    from django.core.management.commands import migrate
    import inspect
    if 'migrate' in inspect.stack()[-1].filename:
        return
    
    # Skip certain models
    skip_models = ['Session', 'LogEntry', 'Migration']
    if sender.__name__ in skip_models:
        return
    
    try:
        AuditLog.objects.create(
            action='DELETE',
            model_name=sender.__name__,
            object_id=instance.id,
            object_repr=str(instance)[:200],
        )
    except:
        # Silently fail during migrations or setup
        pass
