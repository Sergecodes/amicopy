import os
from ckeditor.fields import RichTextField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from core.fields import ReadableShortUUIDField
from core.mixins import UsesCustomSignal
from users.validators import UsernameValidator
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
    display_name_validator = UsernameValidator()

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
    # Used when user issues anonymous transactions
    browser_session_id = models.CharField(max_length=200, blank=True)
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
    deleted_on = models.DateTimeField(null=True, blank=True, editable=False)

    objects = DeviceManager()

    def __str__(self):
        return self.display_name

    def delete(self, really_delete=False):
        """
        delete() isn't called if related objects are deleted via CASCADE. 
        i.e. if a session is deleted, devices will also be deleted.
        """
        if really_delete:
            return super().delete()

        self.deleted_on = timezone.now()
        self.save(update_fields=['deleted_on'])

    @cached_property
    def is_deleted(self):
        return bool(self.deleted_on)
    
    @cached_property
    def has_user(self):
        return bool(self.user)

    @property
    def ongoing_sessions(self):
        """Return the sessions that the user is presently in"""
        return self.sessions.filter(is_active=True, session_device__is_still_present=True)

    def clean(self):
        # Ensure browser_session_id and user aren't both null
        if not self.browser_session_id and not self.user:
            raise ValidationError(
                _("Both the browser session id and user can't be null"),
                code='invalid'
            )

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'transactions\".\"device'
        constraints = [
            models.CheckConstraint(
                check=~Q(browser_session_id='') & Q(user__isnull=True),
                name='browser_session_id_and_user_id_not_both_unset'
            )
        ]


class Transaction(models.Model, TransactionOperations, UsesCustomSignal):
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

    def clean(self):
        # Ensure text_content and files_archive aren't both null
        if not self.text_content and not self.files_archive:
            raise ValidationError(
                _("Both the text content and files archive can't be null"),
                code='invalid'
            )

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)
    
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
        length=12,
        group_by=4,
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
    deleted_by = models.ManyToManyField(
        User,
        through='SessionDelete',
        related_name='deleted_sessions',
        related_query_name='deleted_session'
    )

    def __str__(self):
        return self.title

    @cached_property
    def creator(self):
        return self.creator_device.user

    @property
    def present_devices(self):
        """
        Return devices that are presently in the session. 
        Recall that devices can leave sessions at will
        """
        return self.all_devices.filter(session_device__is_still_present=True)

    @property
    def has_creator_code(self):
        return bool(self.creator_code)

    @property
    def is_ended(self):
        return bool(self.ended_on)

    @property
    def is_expired(self):
        return bool(self.expired_on)

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
    # Whether the device is still in the session
    is_still_present = models.BooleanField(default=True)

    def __str__(self):
        return f'Device {str(self.device)}, session {str(self.session)}'

    def clean(self, **kwargs):
        print(kwargs)
        already_checked = kwargs.get('already_checked')

        # Ensure no two devices have the same names
        if not already_checked:
            can_add, name_found = can_add_device_name(
                self.session.present_devices.values_list('display_name', flat=True),
                self.device.display_name
            )

            if not can_add:
                raise ValidationError(
                    _("Choose another name, there's already a device with the name %s in the session") \
                        % name_found,
                    code='invalid'
                )

    def save(self, *args, **kwargs):
        self.clean(**kwargs)
        return super().save(*args, **kwargs)

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

