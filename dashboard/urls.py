from django.urls import path
from .views import (
    dashboard_view,
    home_view,
    activity_history_view,
    manage_permissions_view,
    update_role_permission_view,
    view_role_permissions_view,
    manage_member_roles_view,
)

urlpatterns = [
    path('', home_view, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('history/', activity_history_view, name='activity_history'),
    path('permissions/', manage_permissions_view, name='manage_permissions'),
    path('permissions/update/', update_role_permission_view, name='update_role_permission'),
    path('permissions/<str:role>/', view_role_permissions_view, name='view_role_permissions'),
    path('admin/manage-member-roles/', manage_member_roles_view, name='manage_member_roles'),
]

