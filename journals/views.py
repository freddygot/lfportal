
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods
import json
from .models import Client, Journal, Appointment
from .forms import ClientForm, JournalForm, AppointmentForm

# Existing views for clients and journals
@login_required
def journal_list(request):
    journals = Journal.objects.all()
    return render(request, 'journals/journal_list.html', {'journals': journals})

@login_required
def journal_detail(request, pk):
    journal = get_object_or_404(Journal, pk=pk)
    return render(request, 'journals/journal_detail.html', {'journal': journal})

@login_required
def journal_create(request):
    if request.method == 'POST':
        form = JournalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('journal_list')
    else:
        form = JournalForm()
    return render(request, 'journals/journal_form.html', {'form': form})

@login_required
def journal_edit(request, pk):
    journal = get_object_or_404(Journal, pk=pk)
    if request.method == 'POST':
        form = JournalForm(request.POST, instance=journal)
        if form.is_valid():
            form.save()
            return redirect('journal_detail', pk=pk)
    else:
        form = JournalForm(instance=journal)
    return render(request, 'journals/journal_form.html', {'form': form})

@login_required
def journal_delete(request, pk):
    journal = get_object_or_404(Journal, pk=pk)
    if request.method == 'POST':
        journal.delete()
        return redirect('journal_list')
    return render(request, 'journals/journal_confirm_delete.html', {'journal': journal})

@login_required
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'journals/client_list.html', {'clients': clients})

@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'journals/client_detail.html', {'client': client})

@login_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'journals/client_form.html', {'form': form})

@login_required
def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_detail', pk=pk)
    else:
        form = ClientForm(instance=client)
    return render(request, 'journals/client_form.html', {'form': form})

@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return render(request, 'journals/client_confirm_delete.html', {'client': client})

# Views for appointments
@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(psychologist=request.user)
    return render(request, 'journals/appointment_list.html', {'appointments': appointments})

@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'journals/appointment_detail.html', {'appointment': appointment})

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'journals/appointment_form.html', {'form': form})

@login_required
def appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_detail', pk=pk)
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'journals/appointment_form.html', {'form': form})

@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointment_list')
    return render(request, 'journals/appointment_confirm_delete.html', {'appointment': appointment})

# API views for FullCalendar
@login_required
def api_appointment_list(request):
    if request.method == 'GET':
        appointments = Appointment.objects.filter(psychologist=request.user)
        data = [
            {
                'id': appointment.id,
                'title': appointment.title,
                'start': f"{appointment.date}T{appointment.time}",
                'client': appointment.client.name,
                'client_id': appointment.client.id,
                'journal_entry_content': appointment.journal_entry.content if appointment.journal_entry else '',
                'journal_entry_id': appointment.journal_entry.id if appointment.journal_entry else None,
                'psychologist': appointment.psychologist.username,
            }
            for appointment in appointments
        ]
        return JsonResponse(data, safe=False)

@csrf_exempt
@login_required
def api_appointment_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            date_time = parse_datetime(data.get('start'))
            date = date_time.date()
            time = date_time.time()
            client_id = data.get('client_id')

            client = Client.objects.get(id=client_id)
            journal_entry_data = data.get('journal_entry')
            if journal_entry_data and journal_entry_data.get('id'):
                journal_entry = Journal.objects.get(id=journal_entry_data['id'])
                journal_entry.content = journal_entry_data['content']
                journal_entry.save()
            else:
                journal_entry = Journal.objects.create(
                    client=client,
                    title=f"Journal for {data.get('title')}",
                    content=journal_entry_data['content'] if journal_entry_data else ''
                )

            appointment = Appointment.objects.create(
                title=data.get('title'),
                psychologist=request.user,
                client=client,
                date=date,
                time=time,
                journal_entry=journal_entry
            )
            return JsonResponse({
                'id': appointment.id,
                'title': appointment.title,
                'start': f"{appointment.date}T{appointment.time}",
                'client': appointment.client.name,
                'client_id': appointment.client.id,
                'journal_entry': {
                    'id': journal_entry.id,
                    'content': journal_entry.content
                },
                'psychologist': appointment.psychologist.username,
            })
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Client.DoesNotExist:
            return JsonResponse({'error': 'Client does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@login_required
@require_http_methods(["PUT"])
def api_appointment_edit(request, pk):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            date_time = parse_datetime(data.get('start'))
            date = date_time.date()
            time = date_time.time()
            appointment = get_object_or_404(Appointment, pk=pk)
            appointment.title = data.get('title')
            appointment.client_id = data.get('client_id')
            appointment.date = date
            appointment.time = time

            journal_entry_data = data.get('journal_entry')
            if journal_entry_data and journal_entry_data.get('id'):
                journal_entry = Journal.objects.get(id=journal_entry_data['id'])
                journal_entry.content = journal_entry_data['content']
                journal_entry.save()
                appointment.journal_entry = journal_entry
            else:
                journal_entry = Journal.objects.create(
                    client=appointment.client,
                    title=f"Journal for {data.get('title')}",
                    content=journal_entry_data['content'] if journal_entry_data else ''
                )
                appointment.journal_entry = journal_entry
            appointment.save()

            return JsonResponse({
                'id': appointment.id,
                'title': appointment.title,
                'start': f"{appointment.date}T{appointment.time}",
                'client': appointment.client.name,
                'client_id': appointment.client.id,
                'journal_entry': {
                    'id': appointment.journal_entry.id,
                    'content': appointment.journal_entry.content
                },
                'psychologist': appointment.psychologist.username,
            })
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Client.DoesNotExist:
            return JsonResponse({'error': 'Client does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
@csrf_exempt
@login_required
@require_http_methods(["DELETE"])
def api_appointment_delete(request, pk):
    try:
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def api_client_list(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        data = [{'id': client.id, 'name': client.name} for client in clients]
        return JsonResponse(data, safe=False)

@login_required
def calendar_view(request):
    return render(request, 'journals/calendar.html')
