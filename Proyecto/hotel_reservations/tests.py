from datetime import date, timedelta
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from hotel_rooms.models import Room
from hotel_services.models import Service

from .models import Reservation, ReservationService


class ReservationRequestTests(TestCase):
    def setUp(self):
        self.room = Room.objects.create(
            number='101',
            name='The Traveler Room',
            short_description='Habitación de prueba.',
            description='Descripción de prueba.',
            cover_image='seed/room-101-traveler.png',
            price_per_night=Decimal('280000.00'),
            capacity=2,
            beds_description='Una cama queen',
            status=Room.Status.AVAILABLE,
        )

    def test_valid_request_saves_total_for_number_of_nights(self):
        check_in = date.today() + timedelta(days=2)
        check_out = check_in + timedelta(days=3)
        response = self.client.post(
            reverse('hotel_reservations:request', args=[self.room.pk]),
            {
                'guest_name': 'Ana López',
                'email': 'ana@example.com',
                'phone': '3000000000',
                'check_in_date': check_in.isoformat(),
                'check_out_date': check_out.isoformat(),
                'guests': 2,
                'notes': '',
            },
            follow=True,
        )

        reservation = Reservation.objects.get()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(reservation.room_total, Decimal('840000.00'))
        self.assertEqual(reservation.estimated_total, Decimal('840000.00'))
        self.assertContains(response, reservation.code)
        self.assertContains(response, 'reservation-confirmation')

    def test_request_rejects_stay_shorter_than_room_minimum(self):
        self.room.min_stay_nights = 3
        self.room.save()
        check_in = date.today() + timedelta(days=2)

        response = self.client.post(
            reverse('hotel_reservations:request', args=[self.room.pk]),
            {
                'guest_name': 'Ana López',
                'email': 'ana@example.com',
                'phone': '3000000000',
                'check_in_date': check_in.isoformat(),
                'check_out_date': (check_in + timedelta(days=2)).isoformat(),
                'guests': 2,
                'notes': '',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Reservation.objects.count(), 0)
        self.assertContains(response, 'estancia mínima de 3 noches')

    def test_unavailable_room_cannot_receive_request(self):
        self.room.status = Room.Status.UNAVAILABLE
        self.room.save()

        response = self.client.get(reverse('hotel_reservations:request', args=[self.room.pk]), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Reservation.objects.count(), 0)
        self.assertContains(response, 'no está disponible')

    def test_editing_dates_recalculates_room_total(self):
        check_in = date.today() + timedelta(days=2)
        reservation = Reservation.objects.create(
            room=self.room,
            guest_name='Ana López',
            email='ana@example.com',
            phone='3000000000',
            check_in_date=check_in,
            check_out_date=check_in + timedelta(days=2),
            guests=2,
        )
        self.assertEqual(reservation.room_total, Decimal('560000.00'))

        reservation.check_out_date = check_in + timedelta(days=5)
        reservation.full_clean()
        reservation.save()
        reservation.refresh_from_db()

        self.assertEqual(reservation.room_total, Decimal('1400000.00'))
        self.assertEqual(reservation.estimated_total, Decimal('1400000.00'))

    def test_service_changes_recalculate_reservation_totals(self):
        check_in = date.today() + timedelta(days=2)
        reservation = Reservation.objects.create(
            room=self.room,
            guest_name='Ana López',
            email='ana@example.com',
            phone='3000000000',
            check_in_date=check_in,
            check_out_date=check_in + timedelta(days=2),
            guests=2,
        )
        service = Service.objects.create(
            name='Masaje',
            short_description='Servicio de prueba.',
            description='Servicio de prueba.',
            image='seed/service-massage.png',
            price=Decimal('50000.00'),
        )
        line = ReservationService.objects.create(
            reservation=reservation,
            service=service,
            quantity=2,
            unit_price=Decimal('50000.00'),
        )
        reservation.refresh_from_db()
        self.assertEqual(reservation.services_total, Decimal('100000.00'))
        self.assertEqual(reservation.estimated_total, Decimal('660000.00'))

        line.delete()
        reservation.refresh_from_db()
        self.assertEqual(reservation.services_total, Decimal('0.00'))
        self.assertEqual(reservation.estimated_total, Decimal('560000.00'))
