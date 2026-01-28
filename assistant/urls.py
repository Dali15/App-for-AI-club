from django.urls import path
from . import views

app_name = 'assistant'

urlpatterns = [
    path('chat/', views.chat_page, name='chat'),
    path('chat/history/', views.chat_history_page, name='chat_history'),
    path('api/send-message/', views.send_message, name='send_message'),
    path('api/history/', views.get_history, name='get_history'),
    path('api/clear-history/', views.clear_history, name='clear_history'),
]
