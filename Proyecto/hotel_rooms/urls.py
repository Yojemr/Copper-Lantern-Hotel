from django.urls import path

from . import views

app_name = 'hotel_rooms'

urlpatterns = [
    path('', views.room_list, name='list'),
]
