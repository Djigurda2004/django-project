from .models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def handle_user_post_save(sender, instance, created, **kwargs):
    pass