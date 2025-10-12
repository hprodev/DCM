from django.core.management.base import BaseCommand
from apps_manager.models import AppCategory

class Command(BaseCommand):
    help = 'Create default app categories'

    def handle(self, *args, **options):
        categories = [
            {'category_name': 'Social', 'description': 'Social media and networking'},
            {'category_name': 'Productivity', 'description': 'Work and organization tools'},
            {'category_name': 'Games', 'description': 'Gaming and entertainment'},
            {'category_name': 'Utilities', 'description': 'System and utility apps'},
            {'category_name': 'Entertainment', 'description': 'Video, music, media'},
        ]
        
        for cat_data in categories:
            category, created = AppCategory.objects.get_or_create(
                category_name=cat_data['category_name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.category_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Category already exists: {category.category_name}'))