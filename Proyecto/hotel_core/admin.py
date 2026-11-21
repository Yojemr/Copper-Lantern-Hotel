from django.contrib import admin

from .models import HeroSlide, Quote, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identidad', {'fields': ('hotel_name', 'short_description', 'description', 'logo', 'is_published')}),
        ('Contacto', {'fields': ('address', 'phone', 'email')}),
        ('Estadía', {'fields': ('check_in_time', 'check_out_time')}),
        ('Redes sociales', {'fields': ('instagram_url', 'facebook_url')}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'subtitle')


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('author', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('author', 'text')

# Register your models here.
