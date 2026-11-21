from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from hotel_services.models import Service

from .models import Room, RoomServiceBenefit


class RoomAvailabilityTests(SimpleTestCase):
    def test_only_active_available_rooms_can_open(self):
        room = Room(is_active=True, status=Room.Status.AVAILABLE)
        coming_soon_room = Room(is_active=True, status=Room.Status.COMING_SOON)
        inactive_room = Room(is_active=False, status=Room.Status.AVAILABLE)

        self.assertTrue(room.is_available)
        self.assertFalse(coming_soon_room.is_available)
        self.assertFalse(inactive_room.is_available)


class RoomBenefitsTests(TestCase):
    def test_inactive_service_is_hidden_from_room_benefits(self):
        room = Room.objects.create(
            number='101', name='Suite de prueba', short_description='Descripción breve',
            description='Descripción completa', cover_image='seed/room.png',
            price_per_night=100000, capacity=2, beds_description='Una cama',
        )
        service = Service.objects.create(
            name='Servicio desactivado', short_description='Descripción breve',
            description='Descripción completa', image='seed/service.png', is_active=False,
        )
        RoomServiceBenefit.objects.create(room=room, service=service)

        response = self.client.get(reverse('hotel_rooms:list'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, service.name)

# Create your tests here.
