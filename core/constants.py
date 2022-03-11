"""Project-wide constants"""

from django.conf import settings
from django.utils.module_loading import import_string

FILE_STORAGE_CLASS = import_string(settings.DEFAULT_FILE_STORAGE)



## SESSION KEYS FORMAT


## CACHE KEYS FORMAT
#
#
#

