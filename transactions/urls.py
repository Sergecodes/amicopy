from django.urls import path 

from . import views 


app_name = 'transactions'


urlpatterns = [
    path('', views.SessionList.as_view(), name='session-list-create'),
    path('verify-uuid/<slug:uuid>/', views.verify_session_exists, name='verify-session'),
    path('verify-code/<str:code>/<slug:uuid>/', views.verify_creator_code, name='verify-code'),
    path('toggle-allow-devices/<slug:uuid>/', views.toggle_allow_new_devices, name='toggle-allow-devices'),

    path('<slug:uuid>/', views.session_detail, name='session-get-delete'),
    
]

