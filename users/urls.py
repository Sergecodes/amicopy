from django.urls import path, include

app_name = 'users'


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),

]
# Default URL: /o/{{ provider }}/
