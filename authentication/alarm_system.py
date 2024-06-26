from django.utils.timezone import now, timedelta
from journals.models import Client, Appointment

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
            alarms[rule.__name__] = rule(self.employee, self.start_date, self.num_weekdays)
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

def rule_no_recent_or_future_appointments(employee, start_date, num_weekdays):
    two_weeks_ago = now() - timedelta(days=14)
    clients = Client.objects.filter(psychologist=employee)

    # Klienter uten nylige avtaler
    clients_without_recent_appointments = clients.exclude(
        appointment__date__gte=two_weeks_ago
    )

    # Klienter uten fremtidige avtaler
    clients_without_future_appointments = clients.exclude(
        appointment__date__gt=now()
    )

    # Finn klienter som oppfyller begge kriteriene
    clients_to_follow_up = clients_without_recent_appointments & clients_without_future_appointments

    return list(clients_to_follow_up)
