from django.contrib.auth import get_user_model
from django.db.models import F
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

from .models.models import Session, Device, Transaction, SessionDevices

User = get_user_model()


@receiver(pre_save, sender=Device)
def set_device_display_name(sender, instance: Device, **kwargs):
    # If device is new and doesn't have display name set, use owner's username if available
    if not instance.pk:
        if not instance.display_name and (owner := instance.user):
            instance.display_name = owner.username


@receiver(post_save, sender=Session)
def set_session_related_attrs(sender, instance: Session, created: bool, **kwargs):
    if created:
        # Add creator device to devices list
        instance.all_devices.add(instance.creator_device_id)

        # Increment session attrs count of creator
        creator = instance.creator
        if creator:
            creator.num_sessions_created = F('num_sessions_created') + 1
            creator.num_sessions_assisted = F('num_sessions_assisted') + 1
            if instance.is_active:
                creator.num_ongoing_sessions = F('num_ongoing_sessions') + 1

            creator.save(update_fields=[
                'num_sessions_created', 'num_sessions_assisted', 'num_ongoing_sessions'
            ])


@receiver(post_save, sender=Transaction)
def set_transaction_related_attrs(sender, instance: Transaction, created: bool, **kwargs):
    if created:
        # Set session last transaction date and number of transactions
        session = instance.session
        session.num_transactions = F('num_transactions') + 1
        session.last_transaction_on = timezone.now()
        session.save(update_fields=['num_transactions', 'last_transaction_on'])

        # Update sender number of transactions sent
        user = instance.from_user
        if user:
            user.num_transactions_sent = F('num_transactions_sent') + 1
            user.save(update_fields=['num_transactions_sent'])


@receiver(post_save, sender=SessionDevices)
def increment_user_sessions_assisted(sender, instance: SessionDevices, created: bool, **kwargs):
    if created:
        # Use received argument from save method
        # instance.user_was_already_in_session  can either be True, False or None
        was_already_in_session = instance.user_was_already_in_session 

        if was_already_in_session is False:
            user = instance.device.user
            if user:
                user.num_sessions_assisted = F('num_sessions_assisted') + 1
                user.num_ongoing_sessions = F('num_ongoing_sessions') + 1
                user.save(update_fields=['num_sessions_assisted', 'num_ongoing_sessions'])


@receiver(post_delete, sender=Session)
def decrement_session_user_attrs(sender, instance: Session, **kwargs):
    # Under normal circumstances, sessions shouldn't be deleted
    creator = instance.creator

    if creator:
        creator.num_sessions_created = F('num_sessions_created') - 1
        creator.num_sessions_assisted = F('num_sessions_assisted') - 1
        creator.save(update_fields=['num_sessions_created', 'num_sessions_assisted'])


@receiver(post_delete, sender=Transaction)
def decrement_transaction_related_attrs(sender, instance: Transaction, **kwargs):
    # Under normal circumstances, transactions shouldn't be deleted
    creator = instance.from_user

    # Update number of transactions
    session = instance.session
    session.num_transactions = F('num_transactions') - 1
    session.save(update_fields=['num_transactions'])

    if creator:
        creator.num_transactions_sent = F('num_transactions_sent') - 1
        creator.save(update_fields=['num_transactions_sent'])


