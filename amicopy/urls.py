
from django.contrib import admin
from django.urls import path, include

from django.utils.translation import gettext_lazy as _


urlpatterns = [
    # path('', include('transactions.urls', namespace='transactions')),
    path(_('sessions/'), include('transactions.urls', namespace='transactions')),
    path('admin/', admin.site.urls),

]

