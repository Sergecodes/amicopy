from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from typing import Iterable


class DeviceOperations:
    def end_session(self, session):
        if not self == session.creator_device:
            raise ValidationError(
                _("Sessions can only be ended by the devices that started them"),
                code='not_permitted'
            )

        session.end()

    def is_in_session(self, session):
        return self in session.all_devices.all()

    def is_session_creator(self, session):
        return self == session.creator_device

    def is_transaction_creator(self, transaction):
        return self == transaction.from_device


class TransactionOperations:
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
    def add_device(self, device):
        """
        Add `device` to the session, session should allow new devices.
        `device` should not yet be saved. 
        """
        from .models import SessionDevices

        # # Validate session key
        # if self.uuid != key:
        #     raise ValidationError(
        #         _('Incorrect key'),
        #         code='invalid_key'
        #     )

        # # Check and validate creator code. If session doesn't have a creator code, 
        # # just ignore. 
        # if self.has_creator_code and self.creator_code != creator_code:
        #     raise ValidationError(
        #         _('Incorrect creator code'),
        #         code='invalid_code'
        #     )

        # Check if device has already been saved
        # (or use if device._state.adding = True)
        if device.pk:
            raise ValidationError(
                _('Device object is already saved, use only unsaved objects'),
                code='invalid'
            )

        # Check whether session accepts new devices
        if not self.accepts_new_devices:
            raise ValidationError(
                _('This session does not accept new devices'),
                code='not_permitted'
            )

        # Check that there's no other device in the session with the same name
        device_names = self.all_devices.values_list('display_name', flat=True)
        if device.display_name in device_names:
            raise ValidationError(
                _("Choose another name, there's already a device with that name in the session"),
                code='invalid'
            )
        
        # Now save device and add to session
        device.save()
        return SessionDevices.objects.create(session=self, device=device)

    def block_new_devices(self):
        self.accepts_new_devices = False
        self.save(update_fields=['accepts_new_devices'])

    def end(self):
        """Mark session as ended"""
        self.ended_on = timezone.now()
        self.save(update_fields=['ended_on'])

    def expire(self):
        """
        Mark session as expired; this will be automatic and will be done based on some rules:
        - All non-premium users' sessions expire after 24hrs(last for 24hrs then expire)
        - Sessions of premium & golden users expire after at least 10hrs of inactivity.

        A cron job can be used to automatically call this method.
        """
        # TODO: set up cron job to call this method; perhaps check sessions after 
        # every 30 mins
        self.expired_on = timezone.now()
        self.save(update_fields=['expired_on'])

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

