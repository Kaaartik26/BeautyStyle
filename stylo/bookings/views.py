from datetime import datetime, timedelta
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render

from services.models import Stylist, Service
from .models import Appointment
from .utils import generate_time_slots

@login_required

def create_appointment(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("invalid req")
    stylist_id = request.POST['stylist_id']
    service_id = request.POST['service_id']
    date = datetime.strptime(request.POST['date'], "%Y-%m-%d").date()
    start_time = datetime.strptime(request.POST['start_time'], "%H:%M").time()

    stylist = get_object_or_404(Stylist, id=stylist_id)
    service = get_object_or_404(Stylist, id=service_id)

    available_slots = generate_time_slots(stylist, service, date)

    valid = False
    for slot_start, slot_end in available_slots:
        if slot_start == start_time:
            end_time = slot_end
            valid = True
            break
    
    if not valid:
        return HttpResponseBadRequest("no slotes available")
    
    with transaction.atomic():
        conflict = Appointment.objects.filter(
            stylist=stylist,
            date=date,
            start_time=start_time,
            status='BOOKED'
        ).exists()

        if conflict:
            return HttpResponseBadRequest("slot already booked")
        
        Appointment.objects.create(
            user=request.user,
            stylist=stylist,
            date=date,
            start_time=start_time,
            end_time=end_time,
            status='BOOKED'
        )
    return redirect('my_appointments')

@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(
        user=request.user
    ).order_by('date', 'start_time')

    return render(request, 'bookings/my_appointments.html', {
        'appointments': appointments
    })

@login_required

def cancel_appointment(request, appointment_id):
    X_HOURS = 2    #random number
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        user=request.user
    )
    if appointment.status != 'BOOKED':
        return HttpResponseBadRequest("No appointments to cancel")
    
    appointment_dt = datetime.combine(
        appointment.date,
        appointment.start_time
    )

    if datetime.now() + timedelta(hours=X_HOURS) > appointment_dt:
        return HttpResponseBadRequest("cancellation time expired! cannot cancel now.")
    
    appointment.status = 'CANCELLED'
    appointment.save()

    return redirect('my_appointments')

def select_date(request):
    return render(request, 'bookings/select_date.html')

def select_slot(request):
    stylist = Stylist.objects.get(id=request.GET['stylist'])
    service = Service.objects.get(id=request.GET['service'])
    date = datetime.strptime(request.GET['date'], "%Y-%m-%d").date()

    slots = generate_time_slots(stylist, service, date)

    return render(request, 'bookings/select_slot.html', {
        'slots': slots,
        'stylist': stylist,
        'service': service,
        'date': date
    })
