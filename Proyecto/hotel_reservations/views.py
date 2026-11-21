from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from hotel_rooms.models import Room

from .forms import ReservationRequestForm


def request_reservation(request, room_id):
    room = get_object_or_404(Room, pk=room_id, is_active=True)
    if not room.is_available:
        messages.error(request, 'Esta habitación no está disponible para recibir solicitudes de reserva.')
        return redirect('hotel_rooms:list')

    if request.method == 'POST':
        form = ReservationRequestForm(request.POST, room=room)
        if form.is_valid():
            reservation = form.save()
            request.session['completed_reservation_id'] = reservation.pk
            return redirect('hotel_reservations:request', room_id=room.pk)
        messages.error(request, 'Revise los campos marcados para enviar la solicitud.')
    else:
        form = ReservationRequestForm(room=room)

    included_services = form.included_services

    completed_reservation = None
    completed_id = request.session.pop('completed_reservation_id', None)
    if completed_id:
        completed_reservation = room.reservations.filter(pk=completed_id).first()
    return render(request, 'hotel_reservations/reservation_request.html', {
        'form': form,
        'room': room,
        'completed_reservation': completed_reservation,
        'service_pricing': form.service_pricing,
        'included_services': included_services,
    })
