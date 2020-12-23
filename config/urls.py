from django.contrib import admin
from django.urls import path, include
from apps.authentication.views import change_password

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.authentication.routers', namespace='authentication')),
    path('api/', include('apps.giveaway.routers', namespace='giveaway')),
    path('accounts/change-password', change_password, name='change_password')
]
