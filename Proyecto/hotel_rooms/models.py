from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


class Room(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Disponible'
        UNAVAILABLE = 'unavailable', 'No disponible'
        COMING_SOON = 'coming_soon', 'Próximamente'
        MAINTENANCE = 'maintenance', 'Mantenimiento'

    number = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    short_description = models.CharField(max_length=220)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='rooms/covers/')
    door_image = models.ImageField(upload_to='rooms/doors/', blank=True)
    mirror_door_image = models.BooleanField(default=False, verbose_name='Voltear imagen de puerta')
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    capacity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    beds_description = models.CharField(max_length=140)
    min_stay_nights = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.AVAILABLE)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'habitación'
        verbose_name_plural = 'habitaciones'
        ordering = ('number',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.number}-{self.name}')
        super().save(*args, **kwargs)

    @property
    def is_available(self):
        return self.is_active and self.status == self.Status.AVAILABLE

    def __str__(self):
        return f'{self.number} - {self.name}'


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='rooms/gallery/')
    alt_text = models.CharField(max_length=180)
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = 'imagen de habitación'
        verbose_name_plural = 'imágenes de habitaciones'
        ordering = ('order', 'id')
        constraints = [models.UniqueConstraint(fields=('room', 'order'), name='unique_room_image_order')]

    def __str__(self):
        return f'Imagen {self.order} de {self.room}'


class RoomServiceBenefit(models.Model):
    class BenefitType(models.TextChoices):
        INCLUDED = 'included', 'Incluido'
        DISCOUNTED = 'discounted', 'Con descuento'
        OPTIONAL = 'optional', 'Opcional'

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='service_benefits')
    service = models.ForeignKey('hotel_services.Service', on_delete=models.PROTECT, related_name='room_benefits')
    benefit_type = models.CharField(max_length=12, choices=BenefitType.choices, default=BenefitType.OPTIONAL)
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))],
    )
    note = models.CharField(max_length=220, blank=True)

    class Meta:
        verbose_name = 'beneficio de habitación'
        verbose_name_plural = 'beneficios de habitaciones'
        constraints = [models.UniqueConstraint(fields=('room', 'service'), name='unique_room_service_benefit')]

    def clean(self):
        errors = {}
        if self.benefit_type == self.BenefitType.DISCOUNTED:
            if self.discount_percentage is None or self.discount_percentage <= 0:
                errors['discount_percentage'] = 'Indica un descuento superior a cero.'
        elif self.discount_percentage is not None:
            errors['discount_percentage'] = 'El descuento solo aplica a beneficios con descuento.'
        if self.service_id and not self.service.can_be_included and self.benefit_type != self.BenefitType.OPTIONAL:
            errors['benefit_type'] = 'Este servicio no puede incluirse ni descontarse en una habitación.'
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f'{self.room} - {self.service} ({self.get_benefit_type_display()})'

# Create your models here.
