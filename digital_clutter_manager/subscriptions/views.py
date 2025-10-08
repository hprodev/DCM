from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Subscription, SubscriptionCategory
from .serializers import SubscriptionSerializer, SubscriptionCreateSerializer, SubscriptionCategorySerializer

class SubscriptionCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubscriptionCategory.objects.all()
    serializer_class = SubscriptionCategorySerializer
    permission_classes = [IsAuthenticated]

class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SubscriptionCreateSerializer
        return SubscriptionSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        active_subs = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(active_subs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def unused(self, request):
        unused_subs = self.get_queryset().filter(
            is_active=True,
            usage_frequency__in=['rarely', 'never']
        )
        serializer = self.get_serializer(unused_subs, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        subscription = self.get_object()
        subscription.cancel()
        serializer = self.get_serializer(subscription)
        return Response(serializer.data)