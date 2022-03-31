from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .constants import (
    API_MESSAGE_TYPE, MAX_NUM_ONGOING_SESSIONS_GOLDEN_USERS, 
    MAX_NUM_ONGOING_SESSIONS_NORMAL_USERS, MAX_NUM_ONGOING_SESSIONS_PREMIUM_USERS, 
    MAX_NUM_ONGOING_SESSIONS_UNAUTH_USERS, 
)


def validate_user_create_session(user):
    """Verify if authed user is permitted to create session"""

    user_num_ongoing_sessions = user.num_ongoing_sessions
    
    if user.is_normal and user_num_ongoing_sessions == (count := MAX_NUM_ONGOING_SESSIONS_NORMAL_USERS):
        raise ValidationError(
            _("You can be in at most %d active session") % count,
            code=API_MESSAGE_TYPE.NOT_PERMITTED.value
        )
    elif user.is_premium and user_num_ongoing_sessions == (count := MAX_NUM_ONGOING_SESSIONS_PREMIUM_USERS):
        raise ValidationError(
            _("You can be in at most %d active sessions") % count,
            code=API_MESSAGE_TYPE.NOT_PERMITTED.value
        )
    elif user.is_golden and user_num_ongoing_sessions == (count := MAX_NUM_ONGOING_SESSIONS_GOLDEN_USERS):
        raise ValidationError(
            _("You can be in at most %d active sessions") % count,
            code=API_MESSAGE_TYPE.NOT_PERMITTED.value
        )
        
        
def validate_user_join_session(user):
    """Verify if authed user is permitted to join session"""
    validate_user_create_session(user)


def validate_device_create_session(device):
    """Verify if device can create session. `device` should have no associated user."""
    if device.num_ongoing_sessions == (count := MAX_NUM_ONGOING_SESSIONS_UNAUTH_USERS):
        raise ValidationError(
            _("You can be in at most %d active session") % count,
            code=API_MESSAGE_TYPE.NOT_PERMITTED.value
        )


def validate_device_join_session(device):
    """Verify if device can join session. `device` should have no associated user."""
    validate_device_create_session(device)



