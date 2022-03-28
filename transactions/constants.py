import enum


MAX_NUM_SESSIONS_UNAUTH_USERS = 1
MAX_NUM_SESSIONS_NORMAL_USERS = 1
MAX_NUM_SESSIONS_PREMIUM_USERS = 2
MAX_NUM_SESSIONS_GOLDEN_USERS = 5

SESSION_UUID_LENGTH = 10
SESSION_UUID_GROUP_BY = 4


class WS_MESSAGE_TYPE(enum.Enum):
    """Message types for use with channels frontend clients"""
    INFO = 'INFO'  
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    REQUEST_JOIN = 'REQUEST_JOIN'
    ENTER = 'ENTER'  
    LEAVE = 'LEAVE'                 # Used when a user leaves a session
    TRANSACTION = 'TRANSACTION'     # Used when there's a new transaction
    SESSION_END = 'SESSION_END'     # Used when creator ends a session

    INVALID_SESSION = 'INVALID_SESSION'
    INVALID_DEVICE = 'INVALID_DEVICE'
    NOT_IN_SESSION = 'NOT_IN_SESSION'


class API_MESSAGE_TYPE(enum.Enum):
    INVALID_CREATOR_CODE = 'INVALID_CREATOR_CODE'
    NO_CREATOR_CODE = 'NO_CREATOR_CODE'
    NOT_PERMITTED = 'NOT_PERMITTED'
    INVALID_SESSION = 'INVALID_SESSION'
    INVALID_DEVICE = 'INVALID_DEVICE'
    NOT_IN_SESSION = 'NOT_IN_SESSION'
    NEW_DEVICES_BLOCKED = 'NEW_DEVICES_BLOCKED'
    NEW_DEVICES_UNBLOCKED = 'NEW_DEVICES_UNBLOCKED'


# # Used in channels
# MSG_TYPE_MESSAGE = 0  	# For standard messages
# MSG_TYPE_WARNING = 1  	# For yellow messages
# MSG_TYPE_DANGER = 2    	# For red & dangerous alerts
# MSG_TYPE_MUTED = 3    	# For just OK information that doesn't bother users
# MSG_TYPE_ENTER = 4    	# For just OK information that doesn't bother users
# MSG_TYPE_LEAVE = 5    	# For just OK information that doesn't bother users

# MESSAGE_TYPES_CHOICES = (
#     (MSG_TYPE_MESSAGE, 'MESSAGE'),
#     (MSG_TYPE_WARNING, 'WARNING'),
#     (MSG_TYPE_DANGER, 'DANGER'),
#     (MSG_TYPE_MUTED, 'MUTED'),
#     (MSG_TYPE_ENTER, 'ENTER'),
#     (MSG_TYPE_LEAVE, 'LEAVE'),
# )

# MESSAGE_TYPES_LIST = [
#     MSG_TYPE_MESSAGE,
#     MSG_TYPE_WARNING,
#     MSG_TYPE_DANGER,
#     MSG_TYPE_MUTED,
#     MSG_TYPE_ENTER,
#     MSG_TYPE_LEAVE,
# ]
