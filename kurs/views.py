from django.shortcuts import render, get_object_or_404
from .models import Kurs, Modul, FullfortModul

def kurs_liste(request):
    kurs = Kurs.objects.all()
    return render(request, 'kurs/kurs_liste.html', {'kurs': kurs})

def kurs_detaljer(request, kurs_id):
    kurs = get_object_or_404(Kurs, pk=kurs_id)
    return render(request, 'kurs/kurs_detaljer.html', {'kurs': kurs})

def modul_detaljer(request, kurs_id, modul_id):
    modul = get_object_or_404(Modul, kurs_id=kurs_id, pk=modul_id)
    return render(request, 'kurs/modul_detaljer.html', {'modul': modul})
