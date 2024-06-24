from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from journals.models import Client, Appointment

@login_required
def dashboard_view(request):
    today = timezone.now().date()
    two_weeks_ago = today - timedelta(weeks=2)
    
    # Hent alle klienter
    clients = Client.objects.all()

    # Filtrer klienter som oppfyller alle tre kriteriene
    clients_without_recent_or_future_appointments = []
    for client in clients:
        # Har hatt minst én avtale tidligere
        past_appointments = Appointment.objects.filter(client=client, date__lte=today)
        
        if past_appointments.exists():
            # Har ikke hatt noen avtale de siste to ukene
            recent_appointments = past_appointments.filter(date__gt=two_weeks_ago)
            
            # Har ingen fremtidige avtaler
            future_appointments = Appointment.objects.filter(client=client, date__gt=today)
            
            if not recent_appointments.exists() and not future_appointments.exists():
                clients_without_recent_or_future_appointments.append(client)

    context = {
        'clients_without_recent_or_future_appointments': clients_without_recent_or_future_appointments
    }

    return render(request, 'dashboard/home.html', context)
