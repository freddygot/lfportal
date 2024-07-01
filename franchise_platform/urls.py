from django.contrib import admin
from django.urls import path, include
from authentication.views import dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('journals/', include('journals.urls')),
    path('kurs/', include('kurs.urls')),
    path('prosedyrer/', include('prosedyrer.urls')),
    path('feedback/', include('feedback.urls')),
    path('', dashboard_view, name='dashboard'),  # Oppdater denne linjen
    path('auth/', include('django.contrib.auth.urls')),  # Dette vil inkludere login, logout, password_change osv.
    path('__debug__/', include('debug_toolbar.urls')),  # Legg til debug toolbar

    

]
