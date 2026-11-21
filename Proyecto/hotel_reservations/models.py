from decimal import Decimal
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum


class Reservation(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendiente'
        CONFIRMED = 'confirmed', 'Confirmada'
        REJECTED = 'rejected', 'Rechazada'
        CANCELLED = 'cancelled', 'Cancelada'

    code = models.CharField(max_length=16, unique=True, editable=False)
    room = models.ForeignKey('hotel_rooms.Room', on_delete=models.PROTECT, related_name='reservations')
    guest_name = models.CharField(max_length=140)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    room_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    services_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    estimated_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'solicitud de reserva'
        verbose_name_plural = 'solicitudes de reserva'
        ordering = ('-created_at',)

    def clean(self):
        errors = {}
        if self.check_in_date and self.check_out_date:
            nights = (self.check_out_date - self.check_in_date).days
            if nights <= 0:
                errors['check_out_date'] = 'La fecha de salida debe ser posterior a la fecha de entrada.'
            elif self.room_id and nights < self.room.min_stay_nights:
                errors['check_out_date'] = (
                    f'Esta habitación requiere una estancia mínima de {self.room.min_stay_nights} '
                    f'noche{"s" if self.room.min_stay_nights != 1 else ""}.'
                )
        if self.room_id:
            if self.guests and self.guests > self.room.capacity:
                errors['guests'] = 'La cantidad de huéspedes supera la capacidad de esta habitación.'
            if not self.room.is_available:
                errors['room'] = 'Solo se pueden solicitar habitaciones disponibles.'
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = f'CL-{uuid4().hex[:8].upper()}'
        if self.room_id and self.check_in_date and self.check_out_date:
            nights = max((self.check_out_date - self.check_in_date).days, 0)
            self.room_total = self.room.price_per_night * Decimal(nights)
        self.estimated_total = self.room_total + self.services_total
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.code} - {self.guest_name}'


class ReservationService(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='selected_services')
    service = models.ForeignKey('hotel_services.Service', on_delete=models.PROTECT, related_name='reservation_lines')
    quantity = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    is_included = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'servicio de reserva'
        verbose_name_plural = 'servicios de reserva'
        constraints = [models.UniqueConstraint(fields=('reservation', 'service'), name='unique_reservation_service')]

    @classmethod
    def refresh_reservation_totals(cls, reservation_id):
        services_total = (
            cls.objects.filter(reservation_id=reservation_id)
            .aggregate(total=Sum('subtotal'))['total']
            or Decimal('0.00')
        )
        Reservation.objects.filter(pk=reservation_id).update(
            services_total=services_total,
            estimated_total=models.F('room_total') + services_total,
        )

    def save(self, *args, **kwargs):
        self.subtotal = Decimal('0.00') if self.is_included else self.unit_price * self.quantity
        super().save(*args, **kwargs)
        self.refresh_reservation_totals(self.reservation_id)

    def delete(self, *args, **kwargs):
        reservation_id = self.reservation_id
        result = super().delete(*args, **kwargs)
        self.refresh_reservation_totals(reservation_id)
        return result

    def __str__(self):
        return f'{self.reservation.code} - {self.service}'

# Create your models here.
