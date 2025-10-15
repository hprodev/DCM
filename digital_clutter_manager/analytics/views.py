from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from subscriptions.models import Subscription
from apps_manager.models import App

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_spending(request):
    user = request.user
    active_subscriptions = Subscription.objects.filter(
        user=user,
        is_active=True
    )
    
    total = sum(sub.monthly_cost for sub in active_subscriptions)
    
    return Response({
        'user': user.username,
        'total_monthly_spending': float(total),
        'currency': 'USD',
        'active_subscriptions_count': active_subscriptions.count()
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def spending_by_category(request):
    user = request.user
    active_subscriptions = Subscription.objects.filter(
        user=user,
        is_active=True
    )
    
    by_category = {}
    for sub in active_subscriptions:
        category = sub.category.category_name
        if category not in by_category:
            by_category[category] = 0
        by_category[category] += float(sub.monthly_cost)
    
    return Response({
        'spending_by_category': by_category,
        'currency': 'USD'
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommendations(request):
    user = request.user
    recommendations = []
    
    # Check for unused subscriptions
    unused_subs = Subscription.objects.filter(
        user=user,
        is_active=True,
        usage_frequency__in=['rarely', 'never']
    )
    
    for sub in unused_subs:
        recommendations.append({
            'type': 'subscription',
            'action': 'cancel',
            'item': sub.subscription_name,
            'reason': f'Used {sub.usage_frequency}',
            'potential_savings': float(sub.monthly_cost)
        })
    
    # Check for unused apps
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    unused_apps = App.objects.filter(
        user=user,
        last_used_date__lt=thirty_days_ago
    )
    
    for app in unused_apps:
        recommendations.append({
            'type': 'app',
            'action': 'delete',
            'item': app.app_name,
            'reason': f'Not used in 30+ days',
            'storage_freed_mb': app.storage_size_mb
        })
    
    # Check for useless apps
    useless_apps = App.objects.filter(
        user=user,
        usefulness_rating='useless'
    )
    
    for app in useless_apps:
        recommendations.append({
            'type': 'app',
            'action': 'delete',
            'item': app.app_name,
            'reason': 'Marked as useless',
            'storage_freed_mb': app.storage_size_mb
        })
    
    return Response({
        'recommendations': recommendations,
        'total_recommendations': len(recommendations)
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    user = request.user
    
    # Subscription stats
    active_subs = Subscription.objects.filter(user=user, is_active=True)
    total_spending = sum(sub.monthly_cost for sub in active_subs)
    unused_subs = active_subs.filter(usage_frequency__in=['rarely', 'never']).count()
    
    # App stats
    all_apps = App.objects.filter(user=user)
    total_storage = sum(app.storage_size_mb for app in all_apps)
    useless_apps = all_apps.filter(usefulness_rating='useless').count()
    
    return Response({
        'user': {
            'username': user.username,
            'email': user.email,
            'preferred_currency': user.profile.preferred_currency
        },
        'subscriptions': {
            'total_active': active_subs.count(),
            'monthly_spending': float(total_spending),
            'unused_count': unused_subs
        },
        'apps': {
            'total_apps': all_apps.count(),
            'total_storage_mb': total_storage,
            'useless_count': useless_apps
        }
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def spending_in_currency(request, currency):
    """
    Convert spending to different currency
    Note: This is a simplified version without external API
    Returns USD values with currency label for now
    """
    user = request.user
    active_subscriptions = Subscription.objects.filter(
        user=user,
        is_active=True
    )
    
    total_usd = sum(sub.monthly_cost for sub in active_subscriptions)
    
    # Simplified: Just return USD value for now
    # You can add external API integration later
    subscriptions_list = []
    for sub in active_subscriptions:
        subscriptions_list.append({
            'name': sub.subscription_name,
            'cost': float(sub.monthly_cost),
            'currency': currency.upper()
        })
    
    return Response({
        'total_spending': float(total_usd),
        'currency': currency.upper(),
        'note': 'Currency conversion feature coming soon',
        'subscriptions': subscriptions_list
    })