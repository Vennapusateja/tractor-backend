from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ['user', 'tractor', 'rating', 'created_at']
    list_filter   = ['rating']
    search_fields = ['user__name', 'tractor__brand']
    raw_id_fields = ['user', 'tractor', 'booking']
