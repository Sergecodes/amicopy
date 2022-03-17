"""Project-wide constants"""

from django.conf import settings
from django.utils.module_loading import import_string


FILE_STORAGE_CLASS = import_string(settings.DEFAULT_FILE_STORAGE)


# Used in channels
MSG_TYPE_MESSAGE = 0  	# For standard messages
MSG_TYPE_WARNING = 1  	# For yellow messages
MSG_TYPE_DANGER = 2    	# For red & dangerous alerts
MSG_TYPE_MUTED = 3    	# For just OK information that doesn't bother users
MSG_TYPE_ENTER = 4    	# For just OK information that doesn't bother users
MSG_TYPE_LEAVE = 5    	# For just OK information that doesn't bother users

MESSAGE_TYPES_CHOICES = (
    (MSG_TYPE_MESSAGE, 'MESSAGE'),
    (MSG_TYPE_WARNING, 'WARNING'),
    (MSG_TYPE_DANGER, 'DANGER'),
    (MSG_TYPE_MUTED, 'MUTED'),
    (MSG_TYPE_ENTER, 'ENTER'),
    (MSG_TYPE_LEAVE, 'LEAVE'),
)

MESSAGE_TYPES_LIST = [
    MSG_TYPE_MESSAGE,
    MSG_TYPE_WARNING,
    MSG_TYPE_DANGER,
    MSG_TYPE_MUTED,
    MSG_TYPE_ENTER,
    MSG_TYPE_LEAVE,
]


## SESSION KEYS FORMAT


## CACHE KEYS FORMAT
#
#
#

