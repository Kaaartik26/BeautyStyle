from django.shortcuts import render
from .models import Service, Stylist

def service_list(request):
    services = Service.objects.all()
    return render(request, 'services/service_list.html', {'services': services})

def stylist_list(request, service_id):
    stylists = Stylist.objects.filter(services=service_id)
    return render(request, 'service/stylist_list.html', {'stylists': stylists})
