# journals/forms.py
from django import forms
from .models import Client, Journal, Appointment

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'psychologist']

class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['client', 'title', 'content']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['title', 'psychologist', 'client', 'date', 'time', 'journal_entry']
