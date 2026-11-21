from django.contrib import admin

from .models import Room, RoomImage, RoomServiceBenefit


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1


class RoomServiceBenefitInline(admin.TabularInline):
    model = RoomServiceBenefit
    extra = 1
    autocomplete_fields = ('service',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'price_per_night', 'capacity', 'status', 'is_featured', 'is_active')
    list_filter = ('status', 'is_featured', 'is_active')
    list_editable = ('status', 'is_featured', 'is_active')
    prepopulated_fields = {'slug': ('number', 'name')}
    search_fields = ('number', 'name', 'short_description', 'description')
    fieldsets = (
        ('Identidad', {'fields': ('number', 'name', 'slug', 'short_description', 'description')}),
        ('Imágenes', {'fields': ('door_image', 'mirror_door_image', 'cover_image')}),
        ('Estadía', {'fields': ('price_per_night', 'capacity', 'beds_description', 'min_stay_nights')}),
        ('Publicación', {'fields': ('status', 'is_featured', 'is_active')}),
    )
    inlines = (RoomImageInline, RoomServiceBenefitInline)

# Register your models here.
