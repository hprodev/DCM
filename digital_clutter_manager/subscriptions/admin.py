from django.contrib import admin
from .models import SubscriptionCategory, Subscription

@admin.register(SubscriptionCategory)
class SubscriptionCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'color_code', 'created_at']
    search_fields = ['category_name']

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['subscription_name', 'user', 'category', 'monthly_cost', 'is_active']
    list_filter = ['is_active', 'billing_cycle', 'category']
    search_fields = ['subscription_name', 'user__username']