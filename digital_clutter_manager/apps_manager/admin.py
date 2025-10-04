from django.contrib import admin
from .models import AppCategory, App

@admin.register(AppCategory)
class AppCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'created_at']
    search_fields = ['category_name']

@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ['app_name', 'user', 'category', 'platform', 'storage_size_mb', 'usefulness_rating']
    list_filter = ['platform', 'usefulness_rating', 'category']
    search_fields = ['app_name', 'user__username']