from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    user    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given')
    tractor = models.ForeignKey('listings.Tractor', on_delete=models.CASCADE, related_name='reviews')
    booking = models.OneToOneField('bookings.Booking', on_delete=models.SET_NULL, null=True, blank=True)

    rating  = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment    = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('user', 'tractor')]
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user.name} on {self.tractor} — {self.rating}★"
