from django.shortcuts import render

from hotel_rooms.models import Room
from hotel_services.models import Service

from .models import HeroSlide, Quote, SiteSettings


def home(request):
    slides = HeroSlide.objects.filter(is_active=True)
    return render(
        request,
        'hotel_core/home.html',
        {
            'site_settings': SiteSettings.objects.filter(is_published=True).first(),
            'hero_slide': slides.first(),
            'slides': slides,
            'featured_rooms': Room.objects.filter(is_active=True, is_featured=True)[:3],
            'featured_services': Service.objects.filter(is_active=True, is_featured=True),
            'quotes': Quote.objects.filter(is_active=True)[:3],
        },
    )

# Create your views here.
