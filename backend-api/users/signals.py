from django.contrib.auth import get_user_model
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from users.models.models import Settings

User = get_user_model()


@receiver(post_save, sender=User)
def create_settings_object(sender, instance: User, created: bool, **kwargs):
    if created:
        Settings.objects.create(user=instance)

