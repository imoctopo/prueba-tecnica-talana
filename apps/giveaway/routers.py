from django.urls import path
from .views import launch_giveaway

app_name = 'giveaway'
urlpatterns = [
    path('giveaway/launch', launch_giveaway, name='launch_giveaway')
]
