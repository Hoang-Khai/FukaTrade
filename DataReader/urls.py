from django.urls import path
from .views import get_history_data

urlpatterns = [
    path('data', get_history_data, name = 'api_history'),
]