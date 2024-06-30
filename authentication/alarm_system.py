from django.utils.timezone import now, timedelta, make_aware
from journals.models import Client, Appointment
from datetime import datetime, time

class AlarmSystem:
    def __init__(self, employee, start_date, num_weekdays):
        self.employee = employee
        self.start_date = start_date
        self.num_weekdays = num_weekdays
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def evaluate(self):
        alarms = {}
        for rule in self.rules:
            try:
                alarms[rule.__name__] = rule(self.employee, self.start_date, self.num_weekdays)
            except TypeError:
                alarms[rule.__name__] = rule(self.employee, self.start_date)
        return alarms

def rule_low_average_patients_per_weekday(employee, start_date, num_weekdays):
    clients = Client.objects.filter(psychologist=employee)
    appointments_last_30_days = Appointment.objects.filter(client__in=clients, date__gte=start_date)
    
    weekday_counts = [0] * 5  # Mandag til fredag
    for appointment in appointments_last_30_days:
        weekday = appointment.date.weekday()
        if weekday < 5:  # Mandag til fredag
            weekday_counts[weekday] += 1

    if num_weekdays > 0:
        average_patients_per_weekday = sum(weekday_counts) / num_weekdays
    else:
        average_patients_per_weekday = 0

    return average_patients_per_weekday < 3.5

def rule_no_recent_or_future_appointments(employee, start_date):
    clients = Client.objects.filter(psychologist=employee)
    end_date = now()

    # Finn klienter uten kommende avtaler
    clients_without_future_appointments = clients.exclude(
        appointment__date__gte=end_date
    ).distinct()

    # Sjekk hver klient for siste avtale og tidspunktet det er to uker etter den avtalen
    exact_two_weeks_alarm_clients = []
    for client in clients_without_future_appointments:
        last_appointment = Appointment.objects.filter(client=client).order_by('-date', '-time').first()
        if last_appointment:
            last_appointment_datetime = make_aware(datetime.combine(last_appointment.date, last_appointment.time))
            if end_date >= last_appointment_datetime + timedelta(days=14):
                exact_two_weeks_alarm_clients.append(client)

    return exact_two_weeks_alarm_clients
