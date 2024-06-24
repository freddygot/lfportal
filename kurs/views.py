# kurs/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Kurs, Modul, FullfortModul

@login_required
def kurs_liste(request):
    kurs = Kurs.objects.all()
    context = {'kurs': kurs}
    return render(request, 'kurs/kurs_liste.html', context)

@login_required
def kurs_detaljer(request, kurs_id):
    kurs = get_object_or_404(Kurs, pk=kurs_id)
    moduler = Modul.objects.filter(kurs=kurs)
    fullforte_moduler = FullfortModul.objects.filter(bruker=request.user, modul__kurs=kurs)
    fullforte_moduler_ids = fullforte_moduler.values_list('modul_id', flat=True)

    total_moduler = moduler.count()
    fullforte_moduler_count = fullforte_moduler.count()
    progresjon = (fullforte_moduler_count / total_moduler) * 100 if total_moduler > 0 else 0

    context = {
        'kurs': kurs,
        'moduler': moduler,
        'fullforte_moduler_ids': fullforte_moduler_ids,
        'progresjon': progresjon
    }
    return render(request, 'kurs/kurs_detaljer.html', context)

@login_required
def fullfor_modul(request, modul_id):
    modul = get_object_or_404(Modul, pk=modul_id)
    FullfortModul.objects.get_or_create(bruker=request.user, modul=modul)
    return redirect('kurs_detaljer', kurs_id=modul.kurs.id)