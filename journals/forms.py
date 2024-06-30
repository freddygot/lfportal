# journals/forms.py
from django import forms
from .models import Client, Journal, Appointment, Service

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'name', 'email', 'birth_date', 'personal_number', 'gender', 
            'address', 'postal_code', 'municipality', 'psychologist'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['client', 'title', 'content']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['title', 'psychologist', 'client', 'date', 'time', 'journal_entry', 'service']
