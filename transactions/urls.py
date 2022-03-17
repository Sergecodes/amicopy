from django.urls import path 
from django.utils.translation import gettext_lazy as _

from . import views 


app_name = 'transactions'


urlpatterns = [
    path('', views.test, name='test'),
    path(_('new/'), views.SessionCreate.as_view(), name='session-create'),
    path('verify-session/', views.verify_session_exists, name='verify-session'),
    path('allow-devices/', views.allow_new_devices, name='allow-devices'),
    path('block-devices/', views.block_new_devices, name='block-devices'),

    path('<slug:uuid>/', views.SessionDetail.as_view(), name='session-detail'),
]

