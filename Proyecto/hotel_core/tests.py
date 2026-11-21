from django.test import TestCase
from django.urls import reverse

from hotel_services.models import Service

from .models import HeroSlide, Quote


class HomeViewTests(TestCase):
    def test_slide_fields_and_active_quote_appear(self):
        HeroSlide.objects.create(
            title='El gran lobby', subtitle='Una bienvenida de madera y luz.',
            image='seed/hero-lobby.png', button_label='Conocer el hotel', button_url='/#hotel',
        )
        Quote.objects.create(text='Texto de prueba', author='Autor de prueba')

        response = self.client.get(reverse('hotel_core:home'))

        self.assertContains(response, 'El gran lobby')
        self.assertContains(response, 'Una bienvenida de madera y luz.')
        self.assertContains(response, 'Conocer el hotel')
        self.assertContains(response, 'Texto de prueba')

    def test_all_active_featured_services_appear(self):
        for index in range(4):
            Service.objects.create(
                name=f'Destacado {index}', short_description='Descripción corta', description='Descripción',
                image='seed/service-spa.png', is_featured=True, is_active=True,
            )
        Service.objects.create(
            name='Destacado oculto', short_description='Descripción corta', description='Descripción',
            image='seed/service-spa.png', is_featured=True, is_active=False,
        )

        response = self.client.get(reverse('hotel_core:home'))

        for index in range(4):
            self.assertContains(response, f'Destacado {index}')
        self.assertNotContains(response, 'Destacado oculto')

    def test_home_is_available_without_seed_data(self):
        response = self.client.get(reverse('hotel_core:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The Copper Lantern Hotel')

    def test_admin_login_uses_branded_template_and_required_fields(self):
        response = self.client.get(reverse('admin:login'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bienvenido al hotel')
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'required')

# Create your tests here.
