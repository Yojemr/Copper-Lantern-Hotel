from datetime import date
from decimal import Decimal
from decimal import ROUND_HALF_UP

from django import forms
from django.db import transaction

from hotel_rooms.models import RoomServiceBenefit
from hotel_services.models import Service

from .models import Reservation, ReservationService


class ReservationServiceChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, service):
        unit_price = self.unit_price_for_instance(service)
        price_display = f'{unit_price:,.0f}'.replace(',', '.')
        return f'{service.name} · COP ${price_display} {service.get_billing_unit_display().lower()}'

    def unit_price_for_instance(self, service):
        benefit = getattr(self, 'benefits_by_service', {}).get(service.pk)
        unit_price = service.price or Decimal('0.00')
        if (
            benefit
            and benefit.benefit_type == RoomServiceBenefit.BenefitType.DISCOUNTED
            and benefit.discount_percentage is not None
        ):
            discount = benefit.discount_percentage / Decimal('100')
            unit_price = (unit_price * (Decimal('1') - discount)).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP,
            )
        return unit_price


class ReservationRequestForm(forms.ModelForm):
    services = ReservationServiceChoiceField(
        queryset=Service.objects.none(),
        required=False,
        label='Servicios adicionales',
        help_text='Los beneficios incluidos en la habitación se agregarán automáticamente.',
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Reservation
        fields = ('guest_name', 'email', 'phone', 'check_in_date', 'check_out_date', 'guests', 'notes')
        labels = {
            'guest_name': 'Nombre del huésped',
            'email': 'Correo electrónico',
            'phone': 'Teléfono',
            'check_in_date': 'Fecha de entrada',
            'check_out_date': 'Fecha de salida',
            'guests': 'Número de huéspedes',
            'notes': 'Notas adicionales',
        }
        widgets = {
            'guest_name': forms.TextInput(attrs={'autocomplete': 'name'}),
            'email': forms.EmailInput(attrs={'autocomplete': 'email'}),
            'phone': forms.TextInput(attrs={'autocomplete': 'tel'}),
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, room, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = room
        self.instance.room = room
        self.benefits_by_service = {
            benefit.service_id: benefit
            for benefit in RoomServiceBenefit.objects.filter(
                room=room,
                service__is_active=True,
                benefit_type__in=(
                    RoomServiceBenefit.BenefitType.INCLUDED,
                    RoomServiceBenefit.BenefitType.DISCOUNTED,
                ),
            ).select_related('service')
        }
        included_ids = [
            service_id for service_id, benefit in self.benefits_by_service.items()
            if (
                benefit.benefit_type == RoomServiceBenefit.BenefitType.INCLUDED
                and benefit.service.can_be_included
            )
        ]
        self.fields['services'].queryset = Service.objects.filter(
            is_active=True, price__isnull=False,
        ).exclude(pk__in=included_ids)
        self.fields['services'].benefits_by_service = self.benefits_by_service

    @property
    def service_pricing(self):
        service_field = self.fields['services']
        return {
            str(service.pk): {
                'price': str(service_field.unit_price_for_instance(service)),
                'unit': service.billing_unit,
            }
            for service in service_field.queryset
        }

    @property
    def included_services(self):
        return [
            benefit.service for benefit in self.benefits_by_service.values()
            if (
                benefit.benefit_type == RoomServiceBenefit.BenefitType.INCLUDED
                and benefit.service.can_be_included
            )
        ]

    def clean_check_in_date(self):
        check_in_date = self.cleaned_data['check_in_date']
        if check_in_date < date.today():
            raise forms.ValidationError('La fecha de entrada no puede estar en el pasado.')
        return check_in_date

    def save(self, commit=True):
        reservation = super().save(commit=False)
        reservation.room = self.room
        nights = (reservation.check_out_date - reservation.check_in_date).days
        reservation.room_total = self.room.price_per_night * Decimal(nights)
        selected_services = list(self.cleaned_data.get('services', ()))
        service_lines = []
        services_total = Decimal('0.00')

        included_benefits = [
            benefit for benefit in self.benefits_by_service.values()
            if benefit.benefit_type == RoomServiceBenefit.BenefitType.INCLUDED
            and benefit.service.can_be_included
        ]
        for benefit in included_benefits:
            service_lines.append((benefit.service, Decimal('0.00'), True))

        for service in selected_services:
            unit_price = self.fields['services'].unit_price_for_instance(service)
            if service.billing_unit == Service.BillingUnit.NIGHT:
                quantity = nights
            elif service.billing_unit == Service.BillingUnit.PERSON:
                quantity = reservation.guests
            else:
                quantity = 1
            services_total += unit_price * quantity
            service_lines.append((service, unit_price, False))

        reservation.services_total = services_total
        reservation.estimated_total = reservation.room_total + reservation.services_total
        if commit:
            with transaction.atomic():
                reservation.save()
                for service, unit_price, is_included in service_lines:
                    if service.billing_unit == Service.BillingUnit.NIGHT:
                        quantity = nights
                    elif service.billing_unit == Service.BillingUnit.PERSON:
                        quantity = reservation.guests
                    else:
                        quantity = 1
                    ReservationService.objects.create(
                        reservation=reservation,
                        service=service,
                        quantity=quantity,
                        unit_price=unit_price,
                        is_included=is_included,
                    )
        return reservation
