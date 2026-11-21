from django.contrib import admin

from .models import Reservation, ReservationService


class ReservationServiceInline(admin.TabularInline):
    model = ReservationService
    extra = 0
    autocomplete_fields = ('service',)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('code', 'guest_name', 'room', 'check_in_date', 'check_out_date', 'guests', 'status', 'estimated_total')
    list_filter = ('status', 'check_in_date', 'check_out_date')
    list_editable = ('status',)
    search_fields = ('code', 'guest_name', 'email', 'phone', 'room__number')
    readonly_fields = ('code', 'room_total', 'services_total', 'estimated_total', 'created_at', 'updated_at')
    inlines = (ReservationServiceInline,)

# Register your models here.
