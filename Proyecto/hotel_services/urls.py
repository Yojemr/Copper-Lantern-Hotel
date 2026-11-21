from django.urls import path

from . import views

app_name = 'hotel_services'

urlpatterns = [
    path('', views.service_list, name='list'),
]
