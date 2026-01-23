from django.shortcuts import render
from .utils import generate_time_slots

def select_slot(request):
    """
    Shows available slots for selected stylist & service (Coming Soon)
    """
    slots = []
    return render(request, 'bookings/select_slot.html', {'slots': slots})
