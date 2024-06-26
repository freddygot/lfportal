from django.urls import path
from . import views

urlpatterns = [
    path('', views.prosedyre_list, name='prosedyre_list'),
    path('<int:pk>/', views.prosedyre_detail, name='prosedyre_detail'),
    path('<int:pk>/start/', views.start_prosedyre, name='start_prosedyre'),
    path('<int:prosedyre_pk>/punkt/<int:punkt_pk>/fullfor/', views.fullfor_punkt, name='fullfor_punkt'),
]
