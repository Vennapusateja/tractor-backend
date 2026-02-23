from rest_framework import serializers
from .models import Review
from users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model  = Review
        fields = ['id', 'user', 'tractor', 'booking', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def validate(self, data):
        request = self.context['request']
        tractor = data['tractor']
        if Review.objects.filter(user=request.user, tractor=tractor).exists():
            raise serializers.ValidationError('You have already reviewed this tractor.')
        # Only farmers who completed a booking can review
        from bookings.models import Booking
        has_completed = Booking.objects.filter(
            farmer=request.user, tractor=tractor, status='completed'
        ).exists()
        if not has_completed:
            raise serializers.ValidationError('You can only review tractors you have used.')
        return data
