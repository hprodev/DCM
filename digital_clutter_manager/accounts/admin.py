from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'preferred_currency', 'email_reminders', 'created_at']
    list_filter = ['preferred_currency', 'email_reminders']
    search_fields = ['user__username', 'user__email']