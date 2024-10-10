from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from .notifications import send_user_creation_notification

@receiver(post_save, sender=User)
def user_created_handler(sender, instance, created, **kwargs):
    if created:
        send_user_creation_notification(instance)
