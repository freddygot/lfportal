from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Feedback
from .tasks import send_feedback_email
from journals.models import Appointment


def feedback_form(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        personal = int(request.POST['personal'])
        interpersonal = int(request.POST['interpersonal'])
        social = int(request.POST['social'])
        general = int(request.POST['general'])
        
        feedback = Feedback(
            client=appointment.client,
            appointment=appointment,
            personal=personal,
            interpersonal=interpersonal,
            social=social,
            general=general
        )
        feedback.save()
        return redirect('success')
    
    return render(request, 'feedback/feedback_form.html', {'appointment': appointment})

def plot_progress(request, client_id):
    import matplotlib.pyplot as plt
    from io import BytesIO
    import base64

    client = get_object_or_404(Client, id=client_id)
    feedbacks = Feedback.objects.filter(client=client).order_by('date')
    
    dates = [f.date for f in feedbacks]
    scores = [f.total_score for f in feedbacks]
    
    plt.figure(figsize=(10, 5))
    plt.plot(dates, scores, marker='o')
    plt.title('Progress Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Score')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    
    return render(request, 'feedback/plot_progress.html', {'graph': graph})


def send_test_email(request):
    appointment_id = 1  # Sett en faktisk avtale-ID her
    send_feedback_email(appointment_id)
    return HttpResponse("Test email sent successfully.")