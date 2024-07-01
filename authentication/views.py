from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
import logging
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.utils.timezone import now, timedelta
from django.contrib.auth.models import User, Group
from journals.models import Client, Appointment
from .models import Profile
from .alarm_system import AlarmSystem, rule_low_average_patients_per_weekday, rule_no_recent_or_future_appointments

# Sett opp logging
logger = logging.getLogger(__name__)

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
def dashboard_view(request):
    user = request.user
    profile = user.profile

    if profile.role == 'franchise_taker':
        return franchise_dashboard_view(request)
    elif profile.role == 'employee':
        return redirect('employee_dashboard', username=user.username)
    else:
        return render(request, 'authentication/dashboard.html', {'error': 'Role not recognized.'})

def get_client_counts_by_group():
    groups = Group.objects.all()
    group_client_counts = {}

    for group in groups:
        psychologists = User.objects.filter(groups=group)
        client_count = Client.objects.filter(psychologist__in=psychologists).count()
        group_client_counts[group.name] = client_count

    return group_client_counts

@login_required
def franchise_dashboard_view(request):
    user = request.user
    profile = user.profile

    # Hent gruppene brukeren tilhører
    groups = user.groups.all()

    # Hent ansatte som tilhører samme gruppe
    employees = User.objects.filter(groups__in=groups).exclude(id=user.id)

    # Print antall ansatte funnet
    print(f"Antall ansatte i samme gruppe som franchisetaker: {employees.count()}")

    # Hent pasienter tilknyttet ansatte i samme gruppe
    clients = Client.objects.filter(psychologist__in=employees)

    # Legg til pasientene til den innloggede franchisetakeren
    own_clients = Client.objects.filter(psychologist=user)
    clients = clients | own_clients

    # Print antall pasienter funnet
    print(f"Antall pasienter: {clients.count()}")

    number_of_patients = clients.count()
    profile.key_metrics['number_of_patients'] = number_of_patients

    # Gjennomsnittlig antall avtaler per pasient
    if number_of_patients > 0:
        total_appointments = Appointment.objects.filter(client__in=clients).count()
        average_appointments_per_patient = total_appointments / number_of_patients
    else:
        average_appointments_per_patient = 0
    profile.key_metrics['average_appointments_per_patient'] = average_appointments_per_patient

    # Gjennomsnittlig antall pasienter per ukedag de siste 30 dagene (mandag til fredag)
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

    # Opprett og evaluer alarmsystemet for hver ansatt
    alarms = []
    for employee in employees:
        alarm_system = AlarmSystem(employee, start_date, num_weekdays)
        alarm_system.add_rule(rule_low_average_patients_per_weekday)
        alarm_system.add_rule(rule_no_recent_or_future_appointments)
        # Legg til flere regler etter behov
        alarm_results = alarm_system.evaluate()
        is_alarm = any(alarm_results.values())
        alarms.append((employee, is_alarm))

    # Calculate the total number of clients per group
    group_client_counts = get_client_counts_by_group()

    return render(request, 'authentication/franchise_dashboard.html', {
        'user': user,
        'profile': profile,
        'groups': groups,
        'alarms': alarms,
        'number_of_patients': number_of_patients,
        'employees': employees,
        'group_client_counts': group_client_counts,
    })

@login_required
def employee_dashboard_view(request, username):
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

    # Gjennomsnittlig antall pasienter per ukedag de siste 30 dagene (mandag til fredag)
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

    # Opprett og evaluer alarmsystemet for brukeren
    alarm_system = AlarmSystem(user, start_date, num_weekdays)
    alarm_system.add_rule(rule_low_average_patients_per_weekday)
    alarm_system.add_rule(rule_no_recent_or_future_appointments)
    # Legg til flere regler etter behov
    alarm_results = alarm_system.evaluate()

    notis = {}
    for key, value in alarm_results.items():
        if value:
            if key == 'rule_no_recent_or_future_appointments':
                notis[key] = value  # Returner klientobjektene
            else:
                notis[key] = value

    return render(request, 'authentication/employee_dashboard.html', {
        'user': user,
        'profile': profile,
        'groups': groups,
        'notis': notis
    })

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard_view')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profiles/edit_profile.html', {'form': form})

@login_required
def franchise_taker_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    return render(request, 'authentication/franchise_taker_profile.html', {'profile': profile})

@login_required
def employee_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    return render(request, 'authentication/employee_profile.html', {'profile': profile})
