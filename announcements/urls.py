```
from django.urls import path
from . import views

urlpatterns = [
    path('',from . import views
_list'),
    path('create/', views.create_announcement, name='create_announcement'),
    path('pending/', views.pending_announcements, name='pending_announcements'),
    path('approve/<int:pk>/', views.approve_announcement, name='approve_announcement'),
    path('reject/<int:pk>/', views.reject_announcement, name='reject_announcement'),
]
```
