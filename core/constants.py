"""Project-wide constants"""
from django.conf import settings
from django.utils.module_loading import import_string


FILE_STORAGE_CLASS = import_string(settings.DEFAULT_FILE_STORAGE)



## SESSION KEYS FORMAT


## CACHE KEYS FORMAT
#  session_<session.uuid>_creator_browser_session_key: Used in websockets SessionConsumer to store
# creator device's browser session id.
#
#  session_<session.uuid>_creator_channel_name: Used in SessionConsumer to store creator device's
# channel name
#
#  device_<device.uuid>_channel_name: Used in SessionConsumer to store device's channel name
# in given connection
#
#

