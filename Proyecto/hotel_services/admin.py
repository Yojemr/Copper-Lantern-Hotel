from django.contrib import admin

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    change_list_template = 'admin/hotel_services/service/change_list.html'
    list_display = ('name', 'price', 'billing_unit', 'duration_minutes', 'can_be_included', 'is_featured', 'is_active')
    list_filter = ('billing_unit', 'can_be_included', 'is_featured', 'is_active')
    list_editable = ('is_featured', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'short_description', 'description')

# Register your models here.
