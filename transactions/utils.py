from channels.db import database_sync_to_async
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from typing import Iterable

from core.exceptions import WSClientError
from .constants import WS_MESSAGE_TYPE, API_MESSAGE_TYPE


def can_add_device_name(existing_device_names: Iterable[str], new_device_name: str):
    """
    Verify if the device with display_name `name` can be added to the session with 
    device names `existing_device_names`.
    Note that there shouldn't be two devices with names such as 'username1' and 'Username1'
    """
    device_names_dict_list = [
        {'lower_name': name.lower(), 'og_name': name} \
        for name in existing_device_names
    ]

    for entry in device_names_dict_list:
        # If name is already taken, return False and the conflicting name
        if new_device_name.lower() == entry['lower_name']:
            return False, entry['og_name']
    
    return True, ''


def get_session_or_404(session_uuid):
    from .models import Session

    try:
        session = Session.objects.get(uuid=session_uuid, is_active=True)
        return True, session
    except Session.DoesNotExist:
        return False, Response({
            'type': API_MESSAGE_TYPE.INVALID_SESSION.value,
            'message': _("This session does not exist or is no longer active")
        }, status=HTTP_404_NOT_FOUND)


# This decorator turns this function from a synchronous function into an async one
# we can call from our async consumers, that handles Django DBs correctly.
# For more, see http://channels.readthedocs.io/en/latest/topics/databases.html
@database_sync_to_async
def get_session_or_error(session_uuid):
    """
    Tries to fetch a session. Raise encountered errors
    """
    from .models.models import Session

    # Find the session they requested (by uuid)
    try:
        return Session.objects.get(uuid=session_uuid, is_active=True)
    except Session.DoesNotExist:
        # NOTE In normal circumstances, the session's existence should be confirmed 
        # before joining the socket; especially in frontend
        raise WSClientError(WS_MESSAGE_TYPE.INVALID_SESSION.value)


@database_sync_to_async
def get_device_or_error(device_uuid):
    """
    Tries to fetch a device. Raise encountered errors
    """
    from .models.models import Device

    # Find the device they requested 
    try:
        return Device.objects.get(uuid=device_uuid)
    except Device.DoesNotExist:
        raise WSClientError(WS_MESSAGE_TYPE.INVALID_DEVICE.value)


@database_sync_to_async
def is_session_creator(device, session):
    return device == session.creator_device


@database_sync_to_async
def get_or_create_device_via_browser(browser_key, **data):
    """
    Try to get a device via its `browser_key`. 
    If not found, create new device.
    `data` should have keys: ip, display_name, user
    """
    from .models.models import Device

    # NOTE that a different browser counts as a different device
    return Device.objects.get_or_create(
        browser_session_key=browser_key, 
        defaults={
            'ip_address': data['ip'],
            'display_name': data['display_name'],
            'user': user if (user := data['user']).is_authenticated else None
        }
    )

