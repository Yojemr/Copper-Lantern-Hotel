from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage


class ContactViewTests(TestCase):
    def test_valid_message_is_saved(self):
        response = self.client.post(
            reverse('hotel_contact:contact'),
            {
                'name': 'Ana López',
                'email': 'ana@example.com',
                'phone': '3000000000',
                'subject': 'Información sobre eventos',
                'message': 'Deseo información para una celebración pequeña.',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertContains(response, 'Su mensaje fue recibido')
