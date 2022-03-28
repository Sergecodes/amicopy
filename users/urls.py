from django.urls import path, include

app_name = 'users'


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),

]

# Default URL: /o/{{ provider }}/

## djoser available endpoints
# /users/
# /users/me/
# /users/confirm/
# /users/resend_activation/
# /users/set_password/
# /users/reset_password/
# /users/reset_password_confirm/
# /users/set_username/
# /users/reset_username/
# /users/reset_username_confirm/
# /token/login/ (Token Based Authentication)
# /token/logout/ (Token Based Authentication)
# /jwt/create/ (JSON Web Token Authentication)
# /jwt/refresh/ (JSON Web Token Authentication)
# /jwt/verify/ (JSON Web Token Authentication)

