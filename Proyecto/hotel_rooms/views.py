from django.shortcuts import render
from itertools import groupby
from django.db.models import Prefetch

from .models import Room, RoomServiceBenefit


def room_list(request):
    rooms = (
        Room.objects.filter(is_active=True)
        .prefetch_related(
            'images',
            Prefetch(
                'service_benefits',
                queryset=RoomServiceBenefit.objects.filter(service__is_active=True).select_related('service'),
                to_attr='visible_service_benefits',
            ),
        )
        .order_by('number')
    )
    floors = []
    for floor, floor_rooms in groupby(rooms, key=lambda room: room.number[0] if room.number and room.number[0].isdigit() else '?'):
        floors.append({'number': floor, 'rooms': list(floor_rooms)})
    return render(request, 'hotel_rooms/room_list.html', {'floors': floors})

# Create your views here.
