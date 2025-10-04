from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class SubscriptionCategory(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    color_code = models.CharField(max_length=7, default='#6366f1')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Subscription Categories'
        ordering = ['category_name']
    
    def __str__(self):
        return self.category_name


class Subscription(models.Model):
    BILLING_CHOICES = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    USAGE_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('rarely', 'Rarely'),
        ('never', 'Never'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey(SubscriptionCategory, on_delete=models.PROTECT, related_name='subscriptions')
    subscription_name = models.CharField(max_length=100)
    monthly_cost = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(max_length=20, choices=BILLING_CHOICES, default='monthly')
    currency = models.CharField(max_length=3, default='USD')
    next_renewal_date = models.DateField()
    usage_frequency = models.CharField(max_length=20, choices=USAGE_CHOICES, default='monthly')
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subscription_name} - {self.user.username}"
    
    def cancel(self):
        self.is_active = False
        self.cancelled_at = timezone.now()
        self.save()