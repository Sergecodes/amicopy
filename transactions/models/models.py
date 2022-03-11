from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from shortuuid.django_fields import ShortUUIDField

from users.validators import UsernameValidator
from .managers import DeviceManager
from .operations import SessionOperations, TransactionOperations, DeviceOperations

User = get_user_model()


def get_sentinel_device():
    """Dummy device used when a device object is deleted"""
    return Device.objects.get_or_create(username='deleted')[0]


def shared_files_upload_path(instance, filename):
	# instance is Transaction about to be saved.
    # File will be uploaded to MEDIA_ROOT/users/user_<id>/artist_posts_photos/<filename>
	# return get_post_media_upload_path(
	# 	instance.post.porter_id,
	# 	ARTIST_POST_PHOTO_UPLOAD_DIR,
	# 	filename
	# )
    # TODO
    pass


class Device(models.Model, DeviceOperations):
    display_name_validator = UsernameValidator()

    ip_address = models.GenericIPAddressField()
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
    browser_session_id = models.CharField(
        max_length=200,
        blank=True
    )
    display_name = models.CharField(
        _('display name'),
        max_length=50,
        help_text=_(
            'Name used to identify you in this session, '
            'users in this session will be able to see this name.'
        ),
        validators=[display_name_validator]
    )
    deleted_on = models.DateTimeField(null=True, blank=True, editable=False)

    objects = DeviceManager()

    def __str__(self):
        return self.display_name

    def delete(self):
        self.deleted_on = timezone.now()
        self.save(update_fields=['deleted_on'])

    @cached_property
    def is_deleted(self):
        return bool(self.deleted_on)

    class Meta:
        db_table = 'transactions\".\"device'


class Transaction(models.Model, TransactionOperations):
    title = models.CharField(
        _('title'),
        help_text=_("Enter a name of at most 100 characters to identify this transaction"),
        max_length=100,
        blank=True
    )
    text_content = models.TextField(
        _('text'),
        help_text=_('Enter the text to share'),
        blank=True
    )
    files_archive = models.FileField(
        # TODO set upload_to path
        upload_to='', 
        validators=[FileExtensionValidator(['zip'])]
    )
    shared_on = models.DateTimeField(auto_now_add=True)
    session = models.ForeignKey(
        'Session',
        db_column='session_id',
        on_delete=models.CASCADE,
        related_name='transactions',
        related_query_name='transaction'
    )
    from_device = models.ForeignKey(
        Device,
        on_delete=models.SET(get_sentinel_device),
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

        to_devices_names = self.to_devices.values_list(
            'device__display_name', flat=True
        ).distinct()
        return _("From %s to %s") % (self.from_device.title, list(to_devices_names))

    class Meta:
        db_table = 'transactions\".\"transaction'


class Session(models.Model, SessionOperations):
    uuid = ShortUUIDField(verbose_name=_('session code'), length=9)
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
    last_active_on = models.DateTimeField(default=timezone.now, editable=False)
    started_on = models.DateTimeField(default=timezone.now, editable=False)
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
        on_delete=models.SET(get_sentinel_device),
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

    class Meta:
        db_table = 'transactions\".\"session'
        contraints = [
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
        related_name='+'
    )
    device = models.ForeignKey(
        Device,
        db_column='device_id',
        on_delete=models.SET(get_sentinel_device),
        related_name='+'
    )
    # When the device joined the session
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Device {str(self.device)}, session {str(self.session)}'

    class Meta:
        db_table = 'transactions\".\"session_with_devices'


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
        on_delete=models.SET(get_sentinel_device),
        related_name='+'
    )

    def __str__(self):
        return f'Device {str(self.device)}, transaction {str(self.transaction)}'

    class Meta:
        db_table = 'transactions\".\"transaction_to_devices'

