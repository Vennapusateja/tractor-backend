from django.db import models
from django.conf import settings


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING   = 'pending',   'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        ACTIVE    = 'active',    'Active'       # Tractor in use
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
        DISPUTED  = 'disputed',  'Disputed'

    class RentType(models.TextChoices):
        HOURLY = 'hourly', 'Per Hour'
        ACRE   = 'acre',   'Per Acre'
        DAILY  = 'daily',  'Per Day'

    tractor = models.ForeignKey(
        'listings.Tractor', on_delete=models.PROTECT, related_name='bookings'
    )
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='bookings'
    )

    # Booking window
    start_date = models.DateField()
    end_date   = models.DateField()
    start_time = models.TimeField(null=True, blank=True)

    # Billing
    rent_type       = models.CharField(max_length=10, choices=RentType.choices)
    quantity        = models.DecimalField(max_digits=8, decimal_places=2, help_text='Hours or Acres')
    price_per_unit  = models.DecimalField(max_digits=8, decimal_places=2)
    driver_required = models.BooleanField(default=False)
    driver_charges  = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_price     = models.DecimalField(max_digits=10, decimal_places=2)

    # Farmer contact for this booking
    contact_phone   = models.CharField(max_length=15, blank=True)
    delivery_address= models.TextField(blank=True)
    notes           = models.TextField(blank=True)

    status     = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking #{self.pk} — {self.farmer.name} → {self.tractor}"

    def calculate_total(self):
        base = self.price_per_unit * self.quantity
        total = base + (self.driver_charges if self.driver_required else 0)
        self.total_price = total
        return total
