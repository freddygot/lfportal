from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy
from django.contrib.auth.models import User, Group
from journals.models import Client, Appointment
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from authentication.models import Profile

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

@login_required
def profile_view(request, username):
    try:
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

        # Beregn gjennomsnittlig antall pasienter per ukedag de siste 30 dagene (mandag til fredag)
        start_date = now() - timedelta(days=30)
        appointments_last_30_days = Appointment.objects.filter(client__in=clients, date__gte=start_date)
        
        weekday_counts = [0] * 5  # Mandag til fredag
        for appointment in appointments_last_30_days:
            weekday = appointment.date.weekday()
            if weekday < 5:  # Mandag til fredag
                weekday_counts[weekday] += 1

        total_weekdays = (now().date() - start_date.date()).days
        num_weeks = total_weekdays // 7
        extra_days = total_weekdays % 7

        # Beregn antall virkedager (mandag til fredag) i de siste 30 dagene
        num_weekdays = num_weeks * 5 + min(extra_days, 5)

        if num_weekdays > 0:
            average_patients_per_weekday = sum(weekday_counts) / num_weekdays
        else:
            average_patients_per_weekday = 0

        # Formater til én desimal
        profile.key_metrics['average_patients_per_weekday'] = format(average_patients_per_weekday, '.1f')

        # Hent gruppene brukeren tilhører
        groups = user.groups.all()

        return render(request, 'authentication/profile.html', {'user': user, 'profile': profile, 'groups': groups})

    except Exception as e:
        # Logg feilen og returner en melding
        print(f"Error in profile_view: {e}")
        return render(request, 'authentication/profile.html', {'error': 'An error occurred while retrieving the profile.'})

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profiles/edit_profile.html', {'form': form})
