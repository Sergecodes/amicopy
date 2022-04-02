from django.urls import path 

from . import views 


app_name = 'transactions'


urlpatterns = [
    path('', views.SessionList.as_view(), name='session-list-create'),
    path('verify-uuid/<slug:uuid>/', views.verify_session_exists, name='verify-session'),
    path('verify-code/<str:code>/<slug:uuid>/', views.verify_creator_code, name='verify-code'),
    path(
        'toggle-allow-devices/<slug:uuid>/', 
        views.toggle_allow_new_devices, 
        name='toggle-allow-devices'
    ),
    path('toggle-pin-session/<slug:uuid>/', views.toggle_pin_session, name='toggle-pin-session'),
    path(
        'toggle-bookmark-transaction/<slug:uuid>/', 
        views.toggle_bookmark_transaction, 
        name='toggle-bookmark-transaction'
    ),
    path('<slug:session_uuid>/transactions/', views.transactions_list, name='transaction-list'),
    path(
        '<slug:session_uuid>/transactions/<slug:transaction_uuid>/', 
        views.transaction_detail, 
        name='transaction-get'
    ),
    
    path('<slug:uuid>/', views.session_detail, name='session-get-delete'),
    
]

