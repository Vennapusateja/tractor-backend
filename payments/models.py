from django.db import models


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING   = 'pending',   'Pending'
        SUCCESS   = 'success',   'Success'
        FAILED    = 'failed',    'Failed'
        REFUNDED  = 'refunded',  'Refunded'

    booking = models.OneToOneField('bookings.Booking', on_delete=models.PROTECT, related_name='payment')
    amount  = models.DecimalField(max_digits=10, decimal_places=2)
    status  = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

    # Razorpay fields
    razorpay_order_id   = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    razorpay_signature  = models.CharField(max_length=255, blank=True)

    failure_reason = models.TextField(blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment #{self.pk} — ₹{self.amount} — {self.status}"
