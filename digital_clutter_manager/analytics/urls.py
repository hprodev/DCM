from django.urls import path
from . import views

urlpatterns = [
    path('spending/', views.monthly_spending, name='monthly-spending'),
    path('spending-by-category/', views.spending_by_category, name='spending-by-category'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('spending/<str:currency>/', views.spending_in_currency, name='spending-in-currency'),
]