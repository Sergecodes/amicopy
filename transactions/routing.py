from django.urls import re_path 

from . import consumers


websocket_urlpatterns = [
    re_path(
        # Let's just use 24 as max for session uuid and max_length for device name
        # to prevent abuse ...
        r'ws/sessions/(?P<session_uuid>[-\w]{1,24})/(?P<device_name>[-\w]{1,50})/$', 
        consumers.SessionConsumer.as_asgi()
    ),
    
]
