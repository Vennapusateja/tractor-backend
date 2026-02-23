from django.db import models
from django.conf import settings


class Tractor(models.Model):
    class Status(models.TextChoices):
        AVAILABLE   = 'available',   'Available'
        RENTED      = 'rented',      'Rented'
        MAINTENANCE = 'maintenance', 'Under Maintenance'
        SOLD        = 'sold',        'Sold'

    class FuelType(models.TextChoices):
        DIESEL  = 'diesel',  'Diesel'
        PETROL  = 'petrol',  'Petrol'
        ELECTRIC= 'electric','Electric'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tractors',
        limit_choices_to={'role__in': ['owner', 'dealer']},
    )

    # Specs
    brand        = models.CharField(max_length=100)          # Mahindra, John Deere…
    model_name   = models.CharField(max_length=100)
    hp           = models.PositiveIntegerField(help_text='Horsepower')
    year         = models.PositiveIntegerField()
    fuel_type    = models.CharField(max_length=10, choices=FuelType.choices, default=FuelType.DIESEL)
    description  = models.TextField(blank=True)

    # Pricing
    rent_price_per_hour = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    rent_price_per_acre = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    sell_price          = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # Availability
    status           = models.CharField(max_length=15, choices=Status.choices, default=Status.AVAILABLE)
    driver_available = models.BooleanField(default=False)
    driver_charges   = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    # Location
    location = models.CharField(max_length=255)
    state    = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    pincode  = models.CharField(max_length=10)
    latitude  = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Meta
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand} {self.model_name} ({self.hp}HP) — {self.owner.name}"

    @property
    def avg_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return None


class TractorImage(models.Model):
    tractor  = models.ForeignKey(Tractor, on_delete=models.CASCADE, related_name='images')
    image    = models.ImageField(upload_to='tractors/images/')
    is_cover = models.BooleanField(default=False)
    order    = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.tractor}"
