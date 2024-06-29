from django.urls import path
from .views import SubmitORSFeedback, ORSProgressGraph, send_test_email, feedback_success

urlpatterns = [
    path('feedback_form/<int:appointment_id>/', SubmitORSFeedback.as_view(), name='feedback_form'),
    path('ors_progress/<int:client_id>/', ORSProgressGraph.as_view(), name='ors_progress'),
    path('send_test_email/', send_test_email, name='send_test_email'),
    path('feedback_success/', feedback_success, name='feedback_success'),
]
