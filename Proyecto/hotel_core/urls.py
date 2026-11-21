from django.urls import path

from . import views

app_name = 'hotel_core'

urlpatterns = [
    path('', views.home, name='home'),
]
