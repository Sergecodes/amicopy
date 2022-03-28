from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from transactions.models.models import Transaction, Session, TransactionBookmark


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
                code='not_permitted'
            )

        # User should not have deleted session
        if session in self.deleted_sessions.all():
            raise ValidationError(
                _('You are not in this session'),
                code='not_permitted'
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
        return self == session.creator_device.user

    def is_transaction_creator(self, transaction: Transaction):
        return self == transaction.from_user 

    def delete_session(self, session: Session):
        """Remove user from list of users that can view session"""
        # User should be in session
        if not session.concerns_user(self):
            raise ValidationError(
                _('You are not in this session'),
                code='not_permitted'
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
                code='not_permitted'
            )

        if not delete_for_all:
            if self.has_deleted_transaction(transaction):
                return 
            return transaction.delete_for_users([self])

        # If we're here, then user wants to delete for all users

        if not self.is_golden:
            raise ValidationError(
                _('You need to have the GOLDEN plan to delete transactions for all users'),
                code='not_permitted'
            )

        if not self.is_transaction_creator(transaction):
            raise ValidationError(
                _('You are not the creator of this transaction'),
                code='not_permitted'
            )
        
        session = transaction.session
        if not session.is_active:
            raise ValidationError(
                _('Sorry, this session is no longer active.'),
                code='not_permitted'
            )

        # User has a GOLDEN plan and they want to delete the transaction for all users
        # who received it(including themself ofcourse)
        target_users = [self]
        target_users.extend(transaction.to_devices.all())
        return transaction.delete_for_users(target_users)
    
    def has_deleted_session(self, session: Session):
        return self in session.deleted_by.all()

    def has_deleted_transaction(self, transaction: Transaction):
        return self in transaction.deleted_by.all()

    def has_bookmarked_transaction(self, transaction: Transaction):
        return self in transaction.bookmarkers.all()

    def bookmark_transaction(self, transaction: Transaction):
        # User should be in transaction
        if not transaction.concerns_user(self):
            raise ValidationError(
                _('You are not in this transaction'),
                code='not_permitted'
            )

        if not self.has_bookmarked_transaction(transaction):
            return TransactionBookmark.objects.create(user=self, transaction=transaction)

    def unbookmark_transaction(self, transaction: Transaction):
        if self.has_bookmarked_transaction(transaction): 
            TransactionBookmark.objects.delete(user=self, transaction=transaction)



