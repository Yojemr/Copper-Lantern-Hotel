from django.test import TestCase
from django.urls import reverse

from .models import Service


class ServiceVisibilityTests(TestCase):
    def test_only_active_services_appear_in_public_catalog(self):
        for name, active in [('Servicio visible', True), ('Servicio oculto', False)]:
            Service.objects.create(
                name=name, short_description='Descripción corta', description='Descripción',
                image='seed/service-spa.png', is_active=active,
            )

        response = self.client.get(reverse('hotel_services:list'))

        self.assertContains(response, 'Servicio visible')
        self.assertNotContains(response, 'Servicio oculto')

# Create your tests here.
