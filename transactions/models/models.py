import os
import shortuuid
# The uuid module is used, though the editor displays it like it isnt...
import uuid
from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from core.fields import ReadableShortUUIDField
from core.mixins import UsesCustomSignal
from users.validators import UsernameValidator
from ..constants import SESSION_UUID_LENGTH, SESSION_UUID_GROUP_BY, API_MESSAGE_TYPE
from ..utils import can_add_device_name
from .managers import DeviceManager
from .operations import SessionOperations, TransactionOperations, DeviceOperations

# Using get_user_model() causes circular import errs
User = settings.AUTH_USER_MODEL


def shared_files_upload_path(instance, filename):
	# instance is Transaction about to be saved.
    # File will be uploaded to MEDIA_ROOT/users/device_<id>/<filename>
    return os.path.join('users', f'device_{instance.from_device_id}', filename)


class Device(models.Model, DeviceOperations, UsesCustomSignal):
    # max length is normally 40chars let's just leave 60 for now
    # see https://docs.djangoproject.com/en/3.2/topics/http/sessions/#extending-database-backed-session-engines
    # see also django.contrib.sessions.models.Session.
    browser_session_key = models.CharField(max_length=60, unique=True, editable=False)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        db_column='user_id',
        related_name='devices',
        related_query_name='device',
        null=True, 
        blank=True
    )
    deleted_on = models.DateTimeField(null=True, blank=True, editable=False)

    objects = DeviceManager()

    def __str__(self):
        return f'{self.uuid}; {self.user}'

    def save(self, *args, **kwargs):
        # If object is still getting created, try to save it.
        # If there's an error because the auto generated uuid value is a duplicate,
        # then regenerate till unique one is obtained.
        # Note however that the chances of having a duplicate uuid are very slim

        uuid = self.uuid
        if not self.pk:
            while True:
                try:
                    Device.objects.get(uuid=uuid)
                except Device.DoesNotExist:
                    # uuid was unique, we can go out of loop
                    break
                else:
                    # uuid wasn't unique. Try again with new uuid.
                    uuid = uuid.uuid4()

        self.uuid = uuid
        super().save(*args, **kwargs)

    def delete(self, really_delete=False):
        """
        delete() isn't called if related objects are deleted via CASCADE. 
        i.e. if a session is deleted, devices will also be deleted.
        """
        if really_delete:
            return super().delete()

        self.deleted_on = timezone.now()
        self.save(update_fields=['deleted_on'])

    @property
    def is_deleted(self):
        return bool(self.deleted_on)
    
    @property
    def has_user(self):
        return bool(self.user)

    @cached_property
    def ongoing_sessions(self):
        """Return the sessions that are active and the device is presently in"""
        return self.sessions.filter(is_active=True, session_device__is_still_present=True)

    @property
    def num_ongoing_sessions(self):
        return self.ongoing_sessions.count()

    def clean(self):
        # Ensure browser_session_key and user aren't both null
        if not self.browser_session_key and not self.user:
            raise ValidationError(
                _("Both the browser session key and user can't be null"),
                code=API_MESSAGE_TYPE.INVALID.value
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'transactions\".\"device'
        constraints = [
            # Either browser_session_key should be set(should not be empty) or
            # user id should not be empty
            # See https://stackoverflow.com/questions/53085645/
            # django-one-of-2-fields-must-not-be-null
            models.CheckConstraint(
                check=~Q(browser_session_key='') | Q(user__isnull=False),
                name='browser_session_key_and_user_id_not_both_unset'
            )
        ]


class Transaction(models.Model, TransactionOperations, UsesCustomSignal):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(
        _('title'),
        help_text=_("Enter a name of at most 100 characters to identify this transaction"),
        max_length=100,
        blank=True
    )
    text_content = RichTextField(
        _('text'),
        help_text=_('Enter the text to share'),
        blank=True
    )
    files_archive = models.FileField(
        upload_to=shared_files_upload_path, 
        validators=[FileExtensionValidator(['zip'])],
        blank=True
    )
    created_on = models.DateTimeField(auto_now_add=True)
    session = models.ForeignKey(
        'Session',
        db_column='session_id',
        on_delete=models.CASCADE,
        related_name='transactions',
        related_query_name='transaction'
    )
    from_device = models.ForeignKey(
        Device,
        on_delete=models.RESTRICT,
        db_column='from_device_id',
        related_name='sent_transactions',
        related_query_name='sent_transaction'
    )
    to_devices = models.ManyToManyField(
        Device,
        through='TransactionToDevices',
        related_name='received_transactions',
        related_query_name='received_transaction'
    )
    deleted_by = models.ManyToManyField(
        User,
        through='TransactionDelete',
        related_name='deleted_transactions',
        related_query_name='deleted_transaction'
    )

    def __str__(self):
        if title := self.title:
            return title

        to_devices_names = self.to_devices.values_list('display_name', flat=True)
        return _("From %s to %s") % (self.from_device.display_name, list(to_devices_names))

    @property
    def group_name(self):
        """
        Returns the Channels Group name that sockets should subscribe to to know
        devices that are concerned in a transaction.
        """
        return 'transaction_%s' % str(self.uuid)

    @cached_property
    def from_user(self):
        return self.from_device.user

    @cached_property
    def to_users(self):
        """Users that received the transaction, same as to_devices but returns users"""
        return get_user_model().active.filter(
            Q(device__deleted_on__isnull=True) & Q(device__in=self.to_devices)
        ).order_by('id').distinct('id')

    def clean(self):
        # Ensure text_content and files_archive aren't both null
        if not self.text_content and not self.files_archive:
            raise ValidationError(
                _("Both the text content and files archive can't be null"),
                code=API_MESSAGE_TYPE.INVALID.value
            )

    def save(self, *args, **kwargs):
        self.clean()
        
        # Ensure uuid is truly unique xD
        uuid = self.uuid
        if not self.pk:
            while True:
                try:
                    Transaction.objects.get(uuid=uuid)
                except Transaction.DoesNotExist:
                    # uuid was unique, we can go out of loop
                    break
                else:
                    # uuid wasn't unique. Try again with new uuid.
                    uuid = uuid.uuid4()

        self.uuid = uuid
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'transactions\".\"transaction'
        constraints = [
            models.CheckConstraint(
                check=~Q(
                    Q(text_content='') & Q(files_archive='')
                ),
                name='text_and_file_not_both_empty'
            )
        ]


class Session(models.Model, SessionOperations, UsesCustomSignal):
    uuid = ReadableShortUUIDField(
        verbose_name=_('session code'), 
        length=SESSION_UUID_LENGTH,
        group_by=SESSION_UUID_GROUP_BY,
        # Just set this as the max length, so that updating the length won't neccessary
        # require a check on all database fields
        max_length=20,
    )
    title = models.CharField(
        _('title'),
        help_text=_("Enter a name of at most 100 characters to identify this session"),
        max_length=100
    )
    creator_code = models.CharField(
        _('your code'),
        max_length=25,
        blank=True,
        help_text=_(
            "Enter a code of at most 25 characters, "
            "other devices will need to enter this code to join the session"
        ),
    )
    accepts_new_devices = models.BooleanField(_('accepts new devices'), default=True)
    last_transaction_on = models.DateTimeField(blank=True, null=True, editable=False)
    is_active = models.BooleanField(default=True)
    started_on = models.DateTimeField(auto_now_add=True)
    ended_on = models.DateTimeField(null=True, blank=True, editable=False)
    expired_on = models.DateTimeField(null=True, blank=True, editable=False)
    all_devices = models.ManyToManyField(
        Device,
        through='SessionDevices',
        related_name='sessions',
        related_query_name='session'
    )
    creator_device = models.ForeignKey(
        Device,
        on_delete=models.RESTRICT,
        db_column='creator_device_id',
        related_name='created_sessions',
        related_query_name='created_session'
    )
    # No "deleted_by" for device since only auth users can delete sessions and if a user 
    # deletes a sessions, it needs to be reflected across all his logged in devices
    deleted_by = models.ManyToManyField(
        User,
        through='SessionDelete',
        related_name='deleted_sessions',
        related_query_name='deleted_session'
    )

    num_transactions = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return f'{self.title}, {self.uuid}'

    @property
    def creator(self):
        return self.creator_device.user

    @cached_property
    def creator_display_name(self):
        return SessionDevices.objects.get(session=self, device=self.creator_device).display_name

    @cached_property
    def present_devices(self):
        """
        Return devices that are presently(still) in the session. 
        Recall that devices can leave sessions at will
        """
        return self.all_devices.filter(session_device__is_still_present=True)

    @property
    def all_users(self):
        """Same as 'all_devices' but returns users"""
        ## See https://docs.djangoproject.com/en/3.2/ref/models/querysets/#distinct
        # "When you specify field names, you must provide an order_by() in the QuerySet, 
        # and the fields in order_by() must start with the fields in distinct(), in the same order."
        return get_user_model().active.filter(
            Q(device__deleted_on__isnull=True) & Q(device__in=self.all_devices.all())
        ).order_by('id').distinct('id')

    @property
    def present_users(self):
        """Same as 'present_devices' but returns users"""
        return get_user_model().active.filter(
            Q(device__deleted_on__isnull=True) & Q(device__in=self.present_devices)
        ).order_by('id').distinct('id')

    @property
    def has_creator_code(self):
        return bool(self.creator_code)

    @property
    def is_ended(self):
        return bool(self.ended_on)

    @property
    def is_expired(self):
        return bool(self.expired_on)
    
    @property
    def group_name(self):
        """
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return 'session_%s' % self.uuid

    def get_absolute_url(self):
        return reverse('transactions:session-detail', kwargs={'uuid': self.uuid})

    def save(self, *args, **kwargs):
        creator_display_name = kwargs['creator_display_name']

        # If object is still getting created, try to save it.
        # If there's an error because the auto generated uuid value is a duplicate,
        # then regenerate till unique one is obtained.
        # Note however that the chances of having a duplicate uuid are very slim

        uuid = self.uuid
        if not self.pk:
            while True:
                try:
                    Session.objects.get(uuid=uuid)
                except Session.DoesNotExist:
                    # Key was unique, we can go out of loop
                    break
                else:
                    # Key wasn't unique. Try again with new key.
                    uuid = shortuuid.random(SESSION_UUID_LENGTH)

        self.uuid = uuid
        super().save(*args, **kwargs)
        
        # Do this so as to pass creator_display_name to post_save signal
        self.creator_display_name = creator_display_name

    class Meta:
        db_table = 'transactions\".\"session'
        constraints = [
            models.UniqueConstraint(
                fields=['uuid'],
                name='unique_session_uuid'
            )
        ]
        indexes = [
			models.Index(
				fields=['title'], 
				name='session_title_idx'
			)
		]


class SessionDevices(models.Model):
    display_name_validator = UsernameValidator()

    session = models.ForeignKey(
        Session,
        db_column='session_id',
        on_delete=models.CASCADE,
        related_name='session_devices',
        related_query_name='session_device'
    )
    device = models.ForeignKey(
        Device,
        db_column='device_id',
        on_delete=models.RESTRICT,
        related_name='session_devices',
        related_query_name='session_device'
    )
    # When the device joined the session
    joined_on = models.DateTimeField(auto_now_add=True)

    # Device name in this session 
    display_name = models.CharField(
        _('display name'),
        max_length=50,
        # "Note that validators will not be run automatically when you save a model, 
        # but if you are using a ModelForm, it will run your validators 
        # on any fields that are included in your form."
        # see https://docs.djangoproject.com/en/3.2/ref/validators/#how-validators-are-run
        validators=[display_name_validator],
        help_text=_(
            'Name used to identify you in this session, '
            'users in this session will be able to see this name.'
        ),
    )

    # Whether the device is still in the session
    is_still_present = models.BooleanField(default=True)

    def __str__(self):
        return f'Device {str(self.device)}, session {str(self.session)}'

    def clean(self, **kwargs):
        already_checked = kwargs.get('already_checked')

        # Session should be active
        if not self.session.is_active:
            raise ValidationError(
                _("Session is no longer active"),
                code=API_MESSAGE_TYPE.INACTIVE_SESSION.value
            )

        # Ensure no two devices have the same name
        if not already_checked:
            can_add, name_found = can_add_device_name(
                self.present_devices.prefetch_related('session_device') \
                .values_list('session_device__display_name', flat=True),
                self.display_name
            )

            if not can_add:
                raise ValidationError(
                    _("Choose another name, there's already a device with the name %s in the session") \
                        % name_found,
                    code=API_MESSAGE_TYPE.IDENTICAL_DEVICE_PRESENT.value
                )

    def save(self, *args, **kwargs):
        self.clean(**kwargs)
        super().save(*args, **kwargs)

        # Pass argument to post-save signal 
        self.user_was_already_in_session = kwargs.get('user_in_session')

    class Meta:
        db_table = 'transactions\".\"session_with_devices'
        constraints = [
			models.UniqueConstraint(
				fields=['session', 'device'],
				name='unique_session_with_device'
			),
		]


class SessionDelete(models.Model):
    session = models.ForeignKey(
        Session,
        db_column='session_id',
        on_delete=models.CASCADE,
        related_name='+'
    )
    user = models.ForeignKey(
        User,
        db_column='user_id',
        on_delete=models.CASCADE,
        related_name='+'
    )
    deleted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{str(self.user)} deleted session {str(self.session)}'

    class Meta:
        db_table = 'transactions\".\"session_delete'
        constraints = [
			models.UniqueConstraint(
				fields=['session', 'user'],
				name='unique_session_delete'
			),
		]


class TransactionToDevices(models.Model):
    transaction = models.ForeignKey(
        Transaction,
        db_column='transaction_id',
        on_delete=models.CASCADE,
        related_name='+'
    )
    device = models.ForeignKey(
        Device,
        db_column='device_id',
        on_delete=models.RESTRICT,
        related_name='+'
    )

    def __str__(self):
        return f'Device {str(self.device)}, transaction {str(self.transaction)}'

    class Meta:
        db_table = 'transactions\".\"transaction_to_devices'
        constraints = [
			models.UniqueConstraint(
				fields=['transaction', 'device'],
				name='unique_transaction_device'
			),
		]


class TransactionBookmark(models.Model):
	transaction = models.ForeignKey(
		Transaction,
		db_column='transaction_id',
		on_delete=models.CASCADE,
		related_name='+'
	)
	bookmarker = models.ForeignKey(
		User,
		db_column='user_id',
		on_delete=models.CASCADE,
		related_name='+'
	)
	bookmarked_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return _('Transaction %s bookmarked by %s') % (self.transaction, self.bookmarker)
	
	class Meta:
		db_table = 'transactions\".\"transaction_bookmark'
		constraints = [
			models.UniqueConstraint(
				fields=['transaction', 'bookmarker'],
				name='unique_transaction_bookmark'
			),
		]


class TransactionDelete(models.Model):
    transaction = models.ForeignKey(
        Transaction,
        db_column='transaction_id',
        on_delete=models.CASCADE,
        related_name='+'
    )
    user = models.ForeignKey(
        User,
        db_column='user_id',
        on_delete=models.CASCADE,
        related_name='+'
    )
    deleted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{str(self.user)} deleted transaction {str(self.transaction)}'

    class Meta:
        db_table = 'transactions\".\"transaction_delete'
        constraints = [
			models.UniqueConstraint(
				fields=['transaction', 'user'],
				name='unique_transaction_delete'
			),
		]

