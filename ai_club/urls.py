"""
URL configuration for ai_club project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import open_admin_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/login/', open_admin_login, name='admin_login'),  # Open admin access
    path('assistant/', include('assistant.urls')),
    path('accounts/', include('accounts.urls')),
    path('events/', include('events.urls')),
    path('announcements/', include('announcements.urls')),
    path('members/', include('members.urls')),
    path('projects/', include('projects.urls')),
    path('', include('dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

