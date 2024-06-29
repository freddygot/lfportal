from django import forms

class FeedbackForm(forms.Form):
    personal = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 10}), label="Personlig: Hvordan jeg har det med meg selv")
    interpersonal = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 10}), label="Mellommenneskelig: Partner, familie og nære relasjoner")
    social = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 10}), label="Sosialt: Arbeid, skole, venner")
    general = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 10}), label="Generelt: Generell opplevelse av hvordan jeg har det")
