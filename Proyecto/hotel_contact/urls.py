from django.urls import path

from . import views

app_name = 'hotel_contact'

urlpatterns = [
    path('', views.contact, name='contact'),
]
