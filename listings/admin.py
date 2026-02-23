from django.contrib import admin
from .models import Tractor, TractorImage


class TractorImageInline(admin.TabularInline):
    model  = TractorImage
    extra  = 1
    fields = ['image', 'is_cover', 'order']


@admin.register(Tractor)
class TractorAdmin(admin.ModelAdmin):
    list_display  = ['brand', 'model_name', 'hp', 'year', 'owner', 'status', 'state', 'is_active']
    list_filter   = ['status', 'is_active', 'state', 'driver_available', 'fuel_type']
    search_fields = ['brand', 'model_name', 'owner__name', 'owner__phone']
    raw_id_fields = ['owner']
    inlines       = [TractorImageInline]
    ordering      = ['-created_at']
