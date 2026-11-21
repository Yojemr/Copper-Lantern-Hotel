from django.urls import path

from . import views

app_name = 'hotel_reservations'

urlpatterns = [
    path('solicitar/<int:room_id>/', views.request_reservation, name='request'),
]
