from django.db import models
from django.conf import settings


class Equipment(models.Model):
    class Type(models.TextChoices):
        PLOW       = 'plow',       'Plow'
        CULTIVATOR = 'cultivator', 'Cultivator'
        SEEDER     = 'seeder',     'Seeder'
        HARVESTER  = 'harvester',  'Harvester'
        SPRAYER    = 'sprayer',    'Sprayer'
        TRAILER    = 'trailer',    'Trailer'
        ROTAVATOR  = 'rotavator',  'Rotavator'
        OTHER      = 'other',      'Other'

    owner       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='equipment')
    name        = models.CharField(max_length=150)
    type        = models.CharField(max_length=20, choices=Type.choices, default=Type.OTHER)
    brand       = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    # Pricing
    rent_price  = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    sell_price  = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Location
    location = models.CharField(max_length=255)
    state    = models.CharField(max_length=100)
    district = models.CharField(max_length=100)

    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.type}) — {self.owner.name}"


class EquipmentImage(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='images')
    image     = models.ImageField(upload_to='equipment/images/')

    def __str__(self):
        return f"Image for {self.equipment}"
