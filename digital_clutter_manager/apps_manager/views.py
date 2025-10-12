from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .permissions import IsOwner
from datetime import timedelta
from .models import App, AppCategory
from .serializers import AppSerializer, AppCreateSerializer, AppCategorySerializer

class AppCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AppCategory.objects.all()
    serializer_class = AppCategorySerializer
    permission_classes = [IsAuthenticated]

class AppViewSet(viewsets.ModelViewSet):
    serializer_class = AppSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return App.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AppCreateSerializer
        return AppSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def unused(self, request):
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        unused_apps = self.get_queryset().filter(
            last_used_date__lt=thirty_days_ago
        )
        serializer = self.get_serializer(unused_apps, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def storage_report(self, request):
        apps = self.get_queryset()
        total_storage = sum(app.storage_size_mb for app in apps)
        
        by_category = {}
        for app in apps:
            category = app.category.category_name
            if category not in by_category:
                by_category[category] = 0
            by_category[category] += app.storage_size_mb
        
        return Response({
            'total_storage_mb': total_storage,
            'by_category': by_category
        })