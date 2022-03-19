from django.urls import path 
from django.utils.translation import gettext_lazy as _

from . import views 


app_name = 'transactions'


urlpatterns = [
    path('', views.test, name='test'),
    
    path(_('new/'), views.SessionCreate.as_view(), name='session-create'),
    path('verify-session/<slug:uuid>/', views.verify_session_exists, name='verify-session'),
    path('verify-code/<str:code>/', views.verify_creator_code, name='verify-code'),
    path('toggle-allow-devices/<slug:uuid>/', views.toggle_allow_new_devices, name='toggle-allow-devices'),

    path('<slug:uuid>/', views.SessionDetail.as_view(), name='session-detail'),
    
]

