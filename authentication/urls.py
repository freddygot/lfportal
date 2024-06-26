from django.urls import path
from .views import register, LoginView
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
]
