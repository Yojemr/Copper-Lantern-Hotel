from django.shortcuts import render

from .models import Service


def service_list(request):
    services = Service.objects.filter(is_active=True).order_by('name')
    return render(request, 'hotel_services/service_list.html', {'services': services})

# Create your views here.
