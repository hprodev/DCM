from rest_framework import serializers
from .models import SubscriptionCategory, Subscription

class SubscriptionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionCategory
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Subscription
        fields = [
            'id', 'user', 'user_username', 'category', 'category_name',
            'subscription_name', 'monthly_cost', 'billing_cycle', 'currency',
            'next_renewal_date', 'usage_frequency', 'is_active', 'notes',
            'created_at', 'cancelled_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'cancelled_at']


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            'category', 'subscription_name', 'monthly_cost', 'billing_cycle',
            'currency', 'next_renewal_date', 'usage_frequency', 'notes'
        ]