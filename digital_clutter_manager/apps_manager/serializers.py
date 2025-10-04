from rest_framework import serializers
from .models import AppCategory, App

class AppCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AppCategory
        fields = '__all__'


class AppSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = App
        fields = [
            'id', 'user', 'user_username', 'category', 'category_name',
            'app_name', 'platform', 'storage_size_mb', 'last_used_date',
            'usefulness_rating', 'install_date', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']


class AppCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = [
            'category', 'app_name', 'platform', 'storage_size_mb',
            'last_used_date', 'usefulness_rating', 'install_date', 'notes'
        ]