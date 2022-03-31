from django.core.exceptions import ValidationError
from django.db.models import F
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from typing import Iterable

from transactions.validators import (
    validate_user_create_session,
    validate_device_create_session
)
from ..constants import API_MESSAGE_TYPE
from ..utils import can_add_device_name


class DeviceOperations:
    def leave_session(self, session):
        """Mark device as no longer in session"""
        from .models import SessionDevices

        try:
            sd_obj = SessionDevices.objects.get(device=self, session=session, session__is_active=True)
        except SessionDevices.DoesNotExist:
            pass
        else:
            sd_obj.is_still_present = False
            sd_obj.save(update_fields=['is_still_present'])

            # If user has no other device in the session, decrement their num_ongoing_sessions
            user = self.user
            if user and user not in session.present_users:
                user.num_ongoing_sessions = F('num_ongoing_sessions') - 1
                user.save(update_fields=['num_ongoing_sessions'])

            # Reset cached property
            try:
                del self.ongoing_sessions
                del session.present_devices
            except AttributeError:
                pass 

    def end_session(self, session):
        if not self == session.creator_device:
            raise ValidationError(
                _("Sessions can only be ended by the device that started them"),
                code=API_MESSAGE_TYPE.NOT_PERMITTED.value
            )

        session.end()

        # Reset cached property
        try:
            del self.ongoing_sessions
        except AttributeError:
            pass 

    def is_presently_in_session(self, session):
        """Is device presently in session"""
        return self in session.present_devices

    def is_session_creator(self, session):
        return self == session.creator_device

    def is_transaction_creator(self, transaction):
        return self == transaction.from_device


class TransactionOperations:
    def concerns_user(self, user):
        """
        Verify if a user partook in a transaction. 
        i.e. if they are the sender or among the receivers
        """
        return user == self.from_user or user in self.to_users

    def delete_for_users(self, users: Iterable):
        """
        Mark transaction as deleted by users `users`. 
        This means the transaction won't be displayed on `users`' list of transactions under 
        given session.

        `users`: iterable of User objects(or ids?)
        """
        from .models import TransactionDelete

        transaction_deletes = []
        for user in users:
            transaction_deletes.append(TransactionDelete(transaction=self, user=user))

        return TransactionDelete.objects.bulk_create(transaction_deletes)


class SessionOperations:
    def concerns_user(self, user):
        """Verify if user partook/is partaking in the session."""
        return user in self.all_users

    def add_device(self, device):
        """
        Add `device` to the session, session should allow new devices. 
        """
        from .models import SessionDevices


        # TODO do max number of sessions verifications on frontend

        user = device.user
        if not user:
            validate_device_create_session(device)
        else:
            validate_user_create_session(user)

        # Check whether session accepts new devices
        if not self.accepts_new_devices:
            raise ValidationError(
                _('This session does not accept new devices'),
                code=API_MESSAGE_TYPE.NOT_PERMITTED.value
            )

        # Check that there's no other device in the session with the same name
        can_add, name_found = can_add_device_name(
            self.present_devices.values_list('display_name', flat=True),
            device.display_name
        )

        if not can_add:
            raise ValidationError(
                _("Choose another name, there's already a device with the name %s in the session") \
                    % name_found,
                code='INVALID'
            )

        # Verify if device user is in session
        # This will be used in the post signal when incrementing user's
        # number of assisted sessions
        user_in_session = None if user is None else user in self.all_users

        # Instantiate class manually instead of calling create object so as to 
        # pass the already_checked argument
        session_device_obj = SessionDevices(session=self, device=device)
        session_device_obj.save(already_checked=True, user_in_session=user_in_session)

        # Reset cached property
        try:
            del device.ongoing_sessions
            del self.present_devices
        except AttributeError:
            pass 

        return session_device_obj

    def allow_new_devices(self):
        if not self.is_active:
            raise ValidationError(
                _('Session is no longer active'),
                code='INVALID'
            )

        if not self.accepts_new_devices:
            self.accepts_new_devices = True
            self.save(update_fields=['accepts_new_devices'])

    def block_new_devices(self):
        if not self.is_active:
            raise ValidationError(
                _('Session is no longer active'),
                code='INVALID'
            )

        if self.accepts_new_devices:
            self.accepts_new_devices = False
            self.save(update_fields=['accepts_new_devices'])

    def end(self):
        """Mark session as ended"""
        if self.is_active:
            self.is_active = False
            self.ended_on = timezone.now()
            self.save(update_fields=['is_active', 'ended_on'])

            # Decrement present users ongoing sessions
            self.present_users.update(num_ongoing_sessions=F('num_ongoing_sessions') - 1)

        # Reset cached property
        try:
            del self.present_devices
        except AttributeError:
            pass 

    def expire(self):
        """
        Mark session as expired; this will be automatic and will be done based on some rules:
        - All non-premium users' sessions expire after 24hrs(last for 24hrs then expire)
        - Sessions of premium & golden users expire after at least 10hrs of inactivity.

        A cron job can be used to automatically call this method.
        """
        # TODO: set up cron job to call this method; perhaps check sessions after 
        # every 30 mins
        if self.is_active:
            self.is_active = False
            self.expired_on = timezone.now()
            self.save(update_fields=['is_active', 'expired_on'])

            # Decrement present users ongoing sessions
            self.present_users.update(num_ongoing_sessions=F('num_ongoing_sessions') - 1)

    def delete_for_users(self, users: Iterable) -> list:
        """
        Mark session as deleted by users `users`. 
        This means the session won't be displayed on `users`' list of sessions;
        just like WhatsApp discussions/chats.

        `users`: iterable of User objects(or ids?)
        """
        from .models import SessionDelete

        session_deletes = []
        for user in users:
            session_deletes.append(SessionDelete(session=self, user=user))

        return SessionDelete.objects.bulk_create(session_deletes)

