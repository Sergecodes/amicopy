from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db.models import Prefetch
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from transactions.constants import API_MESSAGE_TYPE
from transactions.models.models import Transaction, Session, Device, TransactionBookmark


class UserOperations:
    """Mixin containing operations to be used on the User model"""

    def deactivate(self):
        """Mark user as inactive but allow his record in database."""
        # Don't actually delete user's account, mark it as inactive
        if not self.is_active:
            self.deactivated_on = timezone.now()
            self.is_active = False
            self.save(update_fields=['is_active', 'deactivated_on'])

            # Also mark user's "existing" (non deleted) devices as deleted
            self.existing_devices.delete()

    def pin_session(self, session: Session):
        # User should be in session
        if not session.concerns_user(self):
            raise ValidationError(
                _('You are not in this session'),
                code=API_MESSAGE_TYPE.NOT_IN_SESSION.value
            )

        # User should not have deleted session
        if session in self.deleted_sessions.all():
            raise ValidationError(
                _('You are not in this session'),
                code=API_MESSAGE_TYPE.NOT_IN_SESSION.value
            )

        if session != self.pinned_session:
            self.pinned_session = session
            self.save(update_fields=['pinned_session'])

    def unpin_session(self):
        if self.pinned_session:
            self.pinned_session = None
            self.save(update_fields=['pinned_session'])

    def is_presently_in_session(self, session: Session):
        """
        Return whether the user is presently in the session 
        (if the user has any device in the session)
        """
        return self.id in session.present_devices.values_list('user_id', flat=True)

    def is_session_creator(self, session: Session):
        return self == session.creator

    def is_transaction_creator(self, transaction: Transaction):
        return self == transaction.from_user 

    def delete_session(self, session: Session):
        """Remove user from list of users that can view session"""
        # User should be in session
        if not session.concerns_user(self):
            raise ValidationError(
                _('You are not in this session'),
                code=API_MESSAGE_TYPE.NOT_IN_SESSION.value
            )

        if not self.has_deleted_session(session):
            return session.delete_for_users([self])

    def delete_transaction(self, transaction: Transaction, delete_for_all=False):
        """
        Remove user from list of users that can view transaction. 
        If `delete_for_all` is true, user needs to have GOLDEN plan.
        """
        # User should be in transaction
        if not transaction.concerns_user(self):
            raise ValidationError(
                _('You are not in this transaction'),
                code=API_MESSAGE_TYPE.NOT_IN_TRANSACTION.value
            )

        if not delete_for_all:
            if self.has_deleted_transaction(transaction):
                return 
            return transaction.delete_for_users([self])

        ## If we're here, then user wants to delete for all users

        if not self.is_golden:
            raise ValidationError(
                _('You need to have the GOLDEN plan to delete transactions for all users'),
                code=API_MESSAGE_TYPE.NOT_GOLDEN_USER.value
            )

        if not self.is_transaction_creator(transaction):
            raise ValidationError(
                _('You are not the creator of this transaction'),
                code=API_MESSAGE_TYPE.NOT_TRANSACTION_CREATOR.value
            )
        
        session = transaction.session
        if not session.is_active:
            raise ValidationError(
                _('Sorry, this session is no longer active.'),
                code=API_MESSAGE_TYPE.INACTIVE_SESSION.value
            )

        # User has a GOLDEN plan and they want to delete the transaction for all users
        # who received it(including themself ofcourse)
        target_users = [self]
        to_devices = transaction.to_devices.all().select_related('user')
        for device in to_devices:
            user = device.user
            if user:
                target_users.append(user)
            else:
                # Add device deleted transactions uuids to cache.
                # TODO remove this key when session is closed.
                cache_key = f'device_{device.uuid}_deleted_transactions_uuids'
                deleted_uuids = cache.get(cache_key, [])
                deleted_uuids.append(transaction.uuid)
                cache.set(cache_key, deleted_uuids, None)
                
        return transaction.delete_for_users(target_users)
    
    def has_deleted_session(self, session: Session):
        return self in session.deleted_by.all()

    def has_deleted_transaction(self, transaction: Transaction):
        return self in transaction.deleted_by.all()

    def get_transactions(self, session: Session)-> list:
        """Get user's transaction in the session excluding those they deleted"""
        transactions =  Transaction.objects.filter(
            session=session
        ).exclude(
            deleted_transaction__user__in=[self]
        ).select_related(
            'from_device__user'
        ).prefetch_related(
            Prefetch('to_devices', queryset=Device.objects.only('id'))
        )

        user_transactions = []
        for transaction in transactions:
            if transaction.concerns_user(self):
                user_transactions.append(transaction)

        return user_transactions

    def has_bookmarked_transaction(self, transaction: Transaction):
        return self in transaction.bookmarkers.all()

    def bookmark_transaction(self, transaction: Transaction, check=True):
        # User should be in transaction
        if not transaction.concerns_user(self):
            raise ValidationError(
                _('You are not in this transaction'),
                code=API_MESSAGE_TYPE.NOT_IN_TRANSACTION.value
            )

        if check:
            if not self.has_bookmarked_transaction(transaction):
                return TransactionBookmark.objects.create(user=self, transaction=transaction)
        else:
            return TransactionBookmark.objects.create(user=self, transaction=transaction)

    def unbookmark_transaction(self, transaction: Transaction, check=True):
        if check:
            if self.has_bookmarked_transaction(transaction): 
                TransactionBookmark.objects.delete(user=self, transaction=transaction)
        else:
            TransactionBookmark.objects.delete(user=self, transaction=transaction)



