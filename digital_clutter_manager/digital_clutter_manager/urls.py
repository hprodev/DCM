"""
URL configuration for digital_clutter_manager project.

"""
from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/auth/', include('accounts.urls')),
    path('api/subscriptions/', include('subscriptions.urls')),
    path('api/apps/', include('apps_manager.urls')),
    path('api/analytics/', include('analytics.urls')),
]
