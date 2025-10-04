from django.db import models
from django.contrib.auth.models import User

class AppCategory(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'App Categories'
        ordering = ['category_name']
    
    def __str__(self):
        return self.category_name


class App(models.Model):
    PLATFORM_CHOICES = [
        ('iOS', 'iOS'),
        ('Android', 'Android'),
        ('Windows', 'Windows'),
        ('macOS', 'macOS'),
        ('Web', 'Web'),
    ]
    
    RATING_CHOICES = [
        ('useful', 'Useful'),
        ('maybe_useful', 'Maybe Useful'),
        ('useless', 'Useless'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_apps')
    category = models.ForeignKey(AppCategory, on_delete=models.PROTECT, related_name='apps')
    app_name = models.CharField(max_length=100)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    storage_size_mb = models.IntegerField(default=0)
    last_used_date = models.DateField(blank=True, null=True)
    usefulness_rating = models.CharField(max_length=20, choices=RATING_CHOICES, default='useful')
    install_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.app_name} - {self.user.username}"