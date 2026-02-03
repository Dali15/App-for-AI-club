from django.urls import path
from .views import create_event, event_list, register_event, event_detail

urlpatterns = [
    path('create/', create_event, name='create_event'),
    path('', event_list, name='event_list'),
    path('<int:event_id>/', event_detail, name='event_detail'),
    path('register/<int:event_id>/', register_event, name='register_event'),
]
