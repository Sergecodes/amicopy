from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.functional import classproperty, cached_property
from django.utils.translation import gettext_lazy as _

from core.fields import ProperEmailField
from transactions.constants import (
    MAX_NUM_ONGOING_SESSIONS_GOLDEN_USERS,
    MAX_NUM_ONGOING_SESSIONS_NORMAL_USERS,
    MAX_NUM_ONGOING_SESSIONS_PREMIUM_USERS,
)
from transactions.models.models import Session, Transaction, TransactionBookmark
from ..validators import UsernameValidator
from .managers import UserManager
from .operations import UserOperations


class User(AbstractUser, UserOperations):
    username_validator = UsernameValidator()
    first_name, last_name, date_joined = None, None, None

    username = models.CharField(
        _('username'),
        max_length=50,
        unique=True,
        help_text=_(
            'Your username should be not more than 50 characters '
            'and may contain only letters, numbers, hyphens, and underscores; '
            'no other characters are allowed.'
        ),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
            # null, blank, invalid, invalid_choice, unique, unique_for_date
        },
    )
    email = ProperEmailField(
        _('email address'),
        unique=True,
        max_length=50,
        help_text=_(
            "We will send a verification code to this email. \n "
            "You won't be able to change your email."
        ),
    ) 

    # Can user login ? set to False by default 
    # since user has to first confirm ther email address
    is_active = models.BooleanField(default=False)

    # See difference between auto_now_add=True and default=timezone.now:
    # https://stackoverflow.com/questions/59074688/
    # difference-between-auto-now-add-and-timezone-now-as-default-value
    joined_on = models.DateTimeField(_('date joined'), auto_now_add=True)

    deactivated_on = models.DateTimeField(null=True, blank=True, editable=False)
    pinned_session = models.OneToOneField(
        Session,
        on_delete=models.SET_NULL,
        db_column='pinned_session_id',
        related_name='+',
        blank=True,
        null=True
    )
    bookmarked_transactions = models.ManyToManyField(
        Transaction,
        through=TransactionBookmark,
        related_name='bookmarkers',
        related_query_name='bookmarker',
        blank=True
    )

    # From the PermissionsMixin class, just to update related_name attribute of m2m fields
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='users',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='users',
        related_query_name='user',
    )

    num_sessions_created = models.PositiveIntegerField(default=0, editable=False)
    num_sessions_assisted = models.PositiveIntegerField(default=0, editable=False)
    num_transactions_sent = models.PositiveIntegerField(default=0, editable=False)
    # num_transactions_received = models.PositiveIntegerField(default=0, editable=False)
    # The number of active sessions that user is in. (see @property ongoing_sessions)
    num_ongoing_sessions = models.PositiveIntegerField(default=0, editable=False)

    objects = UserManager()

    @classproperty
    def staff(cls):
        return cls.objects.filter(is_staff=True)

    @classproperty
    def staff_users(cls):
        return cls.staff

    @classproperty
    def active(cls):
        return cls.objects.filter(is_active=True)

    @classproperty
    def active_users(cls):
        return cls.active

    @cached_property
    def can_create_session(self):
        user_num_ongoing_sessions = self.num_ongoing_sessions
        if self.is_normal and user_num_ongoing_sessions == MAX_NUM_ONGOING_SESSIONS_NORMAL_USERS:
            return False
        elif self.is_premium and user_num_ongoing_sessions == MAX_NUM_ONGOING_SESSIONS_PREMIUM_USERS:
            return False
        elif self.is_golden and user_num_ongoing_sessions == MAX_NUM_ONGOING_SESSIONS_GOLDEN_USERS:
            return False
            
        return True

    # @property
    # def can_delete_transaction_for_all(self):
    #     """This is similar to the WhatsApp feature (delete message for all)."""
    #     return self.is_golden

    @property
    def existing_devices(self):
        """
        Return the devices that haven't been deleted. 
        All things been normal, devices are "deleted" only when the user is deactivated.
        """
        return self.devices.filter(deleted_on__isnull=True)

    @property
    def all_sessions(self):
        """
        Return ALL the user's sessions. 
        This shouldn't be used to display user's sessions in frontend as it may also return
        sessions that the user has deleted.
        """
        return Session.objects.filter(all_devices__in=self.existing_devices)

    @property
    def created_sessions(self):
        """Return all sessions that user has created"""
        return Session.objects.filter(creator_device__user=self)

    @cached_property
    def undeleted_sessions(self):
        """
        Opposite of self.deleted_sessions but return sessions that 
        user has participated in but hasn't deleted.
        """
        return self.all_sessions.exclude(deleted_by__in=[self])

    @property
    def ongoing_sessions(self):
        """Sessions that user is currently in that are still active"""
        sessions = Session.objects.none()
        existing_devices = self.existing_devices.prefetch_related('sessions')
        for device in existing_devices:
            sessions.union(device.ongoing_sessions)

        return sessions

    @property
    def can_use_rich_text_editor(self):
        """
        Verify if the user can use the rich text editor to set transaction text content.
        Only PREMIUM and GOLDEN user can use it.
        """
        return True if self.is_premium or self.is_golden else False
        
    @property
    def has_pinned_session(self):
        return bool(self.pinned_session)

    @property
    def is_normal(self):
        """User is using the free plan"""
        return not self.is_premium and not self.is_golden

    @property 
    def is_premium(self):
        # TODO
        pass

    @property
    def is_golden(self):
        # TODO
        pass

    def __str__(self):
        return f'{self.username}, {self.email}'

    def delete(self, *args, **kwargs):
        really_delete = kwargs.pop('really_delete', False)

        if really_delete:
            return super().delete(*args, **kwargs)
        
        self.deactivate()

    def clean(self):
        super().clean()

    def save(self, *args, **kwargs):
        # See https://stackoverflow.com/q/4441539/
        # why-doesnt-djangos-model-save-call-full-clean/
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'users\".\"user'
		# Index names cannot be longer than 30 characters.
        indexes = [
			models.Index(
				fields=['is_superuser'], 
				name='user_is_superuser_idx'
			),
            models.Index(
				fields=['is_staff'], 
				name='user_is_staff_idx'
			),
            models.Index(
				fields=['is_active'], 
				name='user_is_active_idx'
			),
		]
    

class Settings(models.Model):
    user = models.OneToOneField(
        User, 
        db_column='user_id',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='settings',
        related_query_name='settings'
    )
    notification_settings = models.JSONField(default=dict)
    site_settings = models.JSONField(default=dict)
    email_settings = models.JSONField(default=dict)

    def __str__(self):
        return f"{str(self.user)}'s settings"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.site_settings = {
                # Hide transaction by default and show only on hover
                'hide_transaction': False
            }

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'users\".\"settings'
        verbose_name = _('settings')
        verbose_name_plural = _('settings')


