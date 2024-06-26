from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Prosedyre, ProsedyrePunkt, ProsedyreGjennomgang

@login_required
def prosedyre_list(request):
    prosedyrer = Prosedyre.objects.all()
    return render(request, 'prosedyrer/prosedyre_list.html', {'prosedyrer': prosedyrer})

@login_required
def prosedyre_detail(request, pk):
    prosedyre = get_object_or_404(Prosedyre, pk=pk)
    punkter = ProsedyrePunkt.objects.filter(prosedyre=prosedyre).order_by('rekkefolge')
    return render(request, 'prosedyrer/prosedyre_detail.html', {'prosedyre': prosedyre, 'punkter': punkter})

@login_required
def start_prosedyre(request, pk):
    prosedyre = get_object_or_404(Prosedyre, pk=pk)
    gjennomgang, created = ProsedyreGjennomgang.objects.get_or_create(bruker=request.user, prosedyre=prosedyre)
    return redirect('prosedyre_detail', pk=prosedyre.pk)

@login_required
def fullfor_punkt(request, prosedyre_pk, punkt_pk):
    prosedyre = get_object_or_404(Prosedyre, pk=prosedyre_pk)
    punkt = get_object_or_404(ProsedyrePunkt, pk=punkt_pk)
    gjennomgang = get_object_or_404(ProsedyreGjennomgang, bruker=request.user, prosedyre=prosedyre)

    # Mark as completed (this is simplified, in a real application you might want more logic here)
    gjennomgang.fullført = True
    gjennomgang.fullført_dato = timezone.now()
    gjennomgang.save()
    
    return redirect('prosedyre_detail', pk=prosedyre.pk)
