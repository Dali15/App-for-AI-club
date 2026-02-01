from django.urls import path
from . import views

urlpatterns = [
    path('', views.member_list, name='member_list'),
    path('<int:user_id>/', views.member_profile, name='member_profile'),
    path('<int:user_id>/manage-role/', views.manage_user_role, name='manage_user_role'),
    path('me/edit/', views.edit_profile, name='edit_profile'),
]
