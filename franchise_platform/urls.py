from django.contrib import admin
from django.urls import path, include
from dashboard.views import dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('journals/', include('journals.urls')),  # Legg til denne linjen
    path('', dashboard_view, name='dashboard'),
    path('kurs/', include('kurs.urls')),  # Legg til denne linjen
]
