from django.core.management.base import BaseCommand
from subscriptions.models import SubscriptionCategory

class Command(BaseCommand):
    help = 'Create default subscription categories'

    def handle(self, *args, **options):
        categories = [
            {'category_name': 'Entertainment', 'description': 'Streaming, music, games', 'color_code': '#e11d48'},
            {'category_name': 'Productivity', 'description': 'Office tools, project management', 'color_code': '#059669'},
            {'category_name': 'Cloud Storage', 'description': 'File storage and backup', 'color_code': '#2563eb'},
            {'category_name': 'Development', 'description': 'Developer tools and hosting', 'color_code': '#dc2626'},
            {'category_name': 'Communication', 'description': 'Email, messaging, video calls', 'color_code': '#7c3aed'},
        ]
        
        for cat_data in categories:
            category, created = SubscriptionCategory.objects.get_or_create(
                category_name=cat_data['category_name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.category_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Category already exists: {category.category_name}'))