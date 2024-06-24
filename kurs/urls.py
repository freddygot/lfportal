from django.urls import path
from . import views

urlpatterns = [
    path('', views.kurs_liste, name='kurs_liste'),
    path('<int:kurs_id>/', views.kurs_detaljer, name='kurs_detaljer'),
    path('<int:kurs_id>/modul/<int:modul_id>/', views.modul_detaljer, name='modul_detaljer'),
]
