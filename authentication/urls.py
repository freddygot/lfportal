from django.urls import path
from . import views  
from .views import LoginView, register, dashboard_view, edit_profile, franchise_taker_profile_view, employee_profile_view

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/franchise/<str:username>/', franchise_taker_profile_view, name='franchise_taker_profile'),
    path('profile/employee/<str:username>/', employee_profile_view, name='employee_profile'),
    path('employee_dashboard/<str:username>/', views.employee_dashboard_view, name='employee_dashboard'),
    path('franchise_dashboard/', views.franchise_dashboard_view, name='franchise_dashboard'),  # Legg til denne linjen
]
