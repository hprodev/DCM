from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.AppCategoryViewSet, basename='app-category')
router.register(r'', views.AppViewSet, basename='app')

urlpatterns = [
    path('', include(router.urls)),
]