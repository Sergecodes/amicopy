
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # path('', include('transactions.urls', namespace='transactions')),
    path('sessions/', include('transactions.urls', namespace='transactions')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

]

