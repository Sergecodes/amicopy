from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

from .models.models import Session, Device, Transaction


@receiver(pre_save, sender=Device)
def set_device_display_name(sender, instance: Device, **kwargs):
    if not instance.display_name and (owner := instance.user):
        instance.display_name = owner.username


@receiver(post_save, sender=Session)
def add_creator_device_to_devices_list(sender, instance: Session, created: bool, **kwargs):
    if created:
        instance.all_devices.add(instance.creator_device_id)


@receiver(post_save, sender=Transaction)
def set_session_last_transaction_date(sender, instance: Transaction, created: bool, **kwargs):
    if created:
        session = instance.session
        session.last_transaction_on = timezone.now()
        session.save(update_fields=['last_transaction_on'])

