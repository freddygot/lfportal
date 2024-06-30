from django.urls import path
from . import views

urlpatterns = [
    # Journal URLs
    path('', views.journal_list, name='journal_list'),
    path('<int:pk>/', views.journal_detail, name='journal_detail'),
    path('new/', views.journal_create, name='journal_create'),
    path('<int:pk>/edit/', views.journal_edit, name='journal_edit'),
    path('<int:pk>/delete/', views.journal_delete, name='journal_delete'),

    # Client URLs
    path('clients/', views.client_list, name='client_list'),
    path('clients/<int:pk>/', views.client_detail, name='client_detail'),
    path('clients/new/', views.client_create, name='client_create'),
    path('clients/<int:pk>/edit/', views.client_edit, name='client_edit'),
    path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),

    # Appointment URLs
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/new/', views.create_appointment, name='create_appointment'),
    path('appointments/<int:pk>/edit/', views.appointment_edit, name='appointment_edit'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),

    # API Endpoints for Calendar
    path('api/appointments/', views.api_appointment_list, name='api_appointment_list'),
    path('api/appointments/create/', views.api_appointment_create, name='api_appointment_create'),
    path('api/appointments/<int:pk>/edit/', views.api_appointment_edit, name='api_appointment_edit'),
    path('api/appointments/<int:pk>/delete/', views.api_appointment_delete, name='api_appointment_delete'),
    path('api/clients/', views.api_client_list, name='api_client_list'),
    path('api/services/', views.api_service_list, name='api_service_list'),

    # Calendar URL
    path('calendar/', views.calendar_view, name='calendar_view'),

    # ORS Progress Graph URL
    path('clients/<int:pk>/ors_progress/', views.client_detail, name='client_ors_progress'),
]
