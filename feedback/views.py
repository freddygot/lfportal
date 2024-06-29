import matplotlib
matplotlib.use('Agg')  # Bruk ikke-interaktiv backend

import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import View
from .models import ORSFeedback
from journals.models import Client, Appointment
from .tasks import send_feedback_email

class SubmitORSFeedback(View):
    def get(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id)
        return render(request, 'feedback/feedback_form.html', {'appointment': appointment})

    def post(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id)
        question_1 = int(request.POST['question_1'])
        question_2 = int(request.POST['question_2'])
        question_3 = int(request.POST['question_3'])
        question_4 = int(request.POST['question_4'])
        
        feedback = ORSFeedback(
            client=appointment.client,
            appointment=appointment,
            question_1=question_1,
            question_2=question_2,
            question_3=question_3,
            question_4=question_4
        )
        feedback.save()
        return redirect('feedback_success')

class ORSProgressGraph(View):
    def get(self, request, client_id):
        client = get_object_or_404(Client, id=client_id)
        feedbacks = ORSFeedback.objects.filter(client=client).order_by('date')

        dates = [feedback.date for feedback in feedbacks]
        scores = [feedback.total_score for feedback in feedbacks]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, scores, marker='o')
        plt.title('ORS Progress Over Time')
        plt.xlabel('Date')
        plt.ylabel('Total Score')
        plt.ylim(0, 40)

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        image_base64 = base64.b64encode(image_png)
        image_base64 = image_base64.decode('utf-8')

        return render(request, 'feedback/plot_progress.html', {'graph': image_base64})

def send_test_email(request):
    appointment_id = 1  # Sett en faktisk avtale-ID her
    send_feedback_email(appointment_id)
    return HttpResponse("Test email sent successfully.")

def feedback_success(request):
    return render(request, 'feedback/success.html')
