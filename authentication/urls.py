from django.urls import path
from .views import register, LoginView
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.profile_view, name='profile'),  # Profilside for innlogget bruker
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('franchise_taker_profile/<str:username>/', views.franchise_taker_profile_view, name='franchise_taker_profile'),
    path('employee_profile/<str:username>/', views.employee_profile_view, name='employee_profile'),
]

