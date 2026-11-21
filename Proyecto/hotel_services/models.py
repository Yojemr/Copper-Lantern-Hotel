from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


class Service(models.Model):
    class BillingUnit(models.TextChoices):
        STAY = 'stay', 'Por estadía'
        NIGHT = 'night', 'Por noche'
        PERSON = 'person', 'Por persona'
        SERVICE = 'service', 'Por servicio'

    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    short_description = models.CharField(max_length=220)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
    )
    billing_unit = models.CharField(max_length=12, choices=BillingUnit.choices, default=BillingUnit.SERVICE)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    can_be_included = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, verbose_name='Destacado en inicio', help_text='Muestra este servicio en la sección de servicios del inicio.')
    is_active = models.BooleanField(default=True, verbose_name='Visible en el sitio', help_text='Si se desactiva, desaparece del catálogo público y de los destacados.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'servicio'
        verbose_name_plural = 'servicios'
        ordering = ('name',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Create your models here.
