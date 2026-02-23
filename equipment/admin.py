from django.contrib import admin
from .models import Equipment, EquipmentImage


class EquipmentImageInline(admin.TabularInline):
    model = EquipmentImage
    extra = 1


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display  = ['name', 'type', 'owner', 'state', 'rent_price', 'sell_price', 'is_active']
    list_filter   = ['type', 'is_active', 'state']
    search_fields = ['name', 'owner__name']
    inlines       = [EquipmentImageInline]
