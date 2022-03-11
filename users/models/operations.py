from django.core.exceptions import ValidationError
from django.db.models import F
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from notifications.models.models import Notification
from notifications.signals import notify


class UserOperations:
    """Mixin containing operations to be used on the User model"""

    def deactivate(self):
        """Mark user as inactive but allow his record in database."""

        # Don't actually delete user's account, mark it as inactive
        self.deactivated_on = timezone.now()
        self.is_active = False
        self.save(update_fields=['is_active', 'deactivated_on'])

        # Also mark user's devices as deleted
        self.devices.delete()



