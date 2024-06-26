from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from journals.models import Client, Appointment  # Importer Client- og Appointment-modellene




def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})

class LoginView(DjangoLoginView):
    template_name = 'authentication/login.html'


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile

    # Antall pasienter
    clients = Client.objects.filter(psychologist=user)
    number_of_patients = clients.count()
    profile.key_metrics['number_of_patients'] = number_of_patients

    # Gjennomsnittlig antall avtaler per pasient
    if number_of_patients > 0:
        total_appointments = Appointment.objects.filter(client__in=clients).count()
        average_appointments_per_patient = total_appointments / number_of_patients
    else:
        average_appointments_per_patient = 0
    profile.key_metrics['average_appointments_per_patient'] = average_appointments_per_patient

    return render(request, 'authentication/profile.html', {'user': user})