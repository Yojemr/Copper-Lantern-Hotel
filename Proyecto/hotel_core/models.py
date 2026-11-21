from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class SiteSettings(models.Model):
    hotel_name = models.CharField(max_length=120, default='The Copper Lantern Hotel')
    short_description = models.CharField(max_length=220)
    description = models.TextField()
    logo = models.ImageField(upload_to='site/', blank=True)
    address = models.CharField(max_length=220)
    phone = models.CharField(max_length=40)
    email = models.EmailField()
    check_in_time = models.TimeField()
    check_out_time = models.TimeField()
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'configuración del sitio'
        verbose_name_plural = 'configuración del sitio'

    def clean(self):
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError('Solo puede existir una configuración general del hotel.')

    def __str__(self):
        return self.hotel_name


class HeroSlide(models.Model):
    title = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=220)
    image = models.ImageField(upload_to='hero/')
    button_label = models.CharField(max_length=40, blank=True)
    button_url = models.CharField(max_length=240, blank=True)
    order = models.PositiveSmallIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'diapositiva principal'
        verbose_name_plural = 'diapositivas principales'
        ordering = ('order', 'id')

    def __str__(self):
        return self.title


class Quote(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=120)
    author_description = models.CharField(max_length=160, blank=True)
    source_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='quotes/', blank=True)
    attribution = models.CharField(max_length=220, blank=True)
    order = models.PositiveSmallIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'cita'
        verbose_name_plural = 'citas'
        ordering = ('order', 'id')

    def __str__(self):
        return f'{self.author}: {self.text[:50]}'

# Create your models here.
