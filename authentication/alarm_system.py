# authentication/alarm_system.py
from datetime import timedelta
from django.utils.timezone import now
from journals.models import Appointment, Client

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

# Regler for alarmsystemet
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

# Eksempel på flere regler som kan legges til senere
def another_rule_example(employee, start_date, num_weekdays):
    # Her kan du legge til logikk for en annen regel
    return False
