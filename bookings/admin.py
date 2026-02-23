from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display  = ['id', 'farmer', 'tractor', 'start_date', 'end_date', 'total_price', 'status']
    list_filter   = ['status', 'rent_type', 'driver_required']
    search_fields = ['farmer__name', 'farmer__phone', 'tractor__brand']
    raw_id_fields = ['farmer', 'tractor']
    ordering      = ['-created_at']
