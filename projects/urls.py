from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('create/', views.create_project, name='create_project'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('<int:project_id>/delete/', views.delete_project, name='delete_project'),
    path('<int:project_id>/add-file/', views.add_file, name='add_file'),
    path('file/<int:file_id>/delete/', views.delete_file, name='delete_file'),
    path('<int:project_id>/add-update/', views.add_update, name='add_update'),
]
