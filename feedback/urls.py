from django.urls import path
from . import views
from .views import send_test_email

urlpatterns = [
    path('feedback/<int:appointment_id>/', views.feedback_form, name='feedback_form'),
    path('plot_progress/<int:client_id>/', views.plot_progress, name='plot_progress'),
    path('send-test-email/', views.send_test_email, name='send_test_email'),
]
