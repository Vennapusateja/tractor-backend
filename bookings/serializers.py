from rest_framework import serializers
from .models import Booking
from listings.serializers import TractorSerializer
from users.serializers import UserSerializer


class BookingSerializer(serializers.ModelSerializer):
    tractor = TractorSerializer(read_only=True)
    farmer  = UserSerializer(read_only=True)

    class Meta:
        model  = Booking
        fields = '__all__'
        read_only_fields = ['id', 'farmer', 'total_price', 'status', 'created_at']


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Booking
        fields = [
            'tractor', 'start_date', 'end_date', 'start_time',
            'rent_type', 'quantity', 'driver_required',
            'contact_phone', 'delivery_address', 'notes',
        ]

    def validate(self, data):
        tractor = data['tractor']
        if tractor.status != 'available':
            raise serializers.ValidationError('This tractor is not available for booking.')
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError('Start date must be before end date.')
        return data

    def create(self, validated_data):
        tractor = validated_data['tractor']
        rent_type = validated_data['rent_type']
        quantity  = validated_data['quantity']

        # Set price per unit based on rent type
        if rent_type == 'hourly':
            price_per_unit = tractor.rent_price_per_hour or 0
        elif rent_type == 'acre':
            price_per_unit = tractor.rent_price_per_acre or 0
        else:
            price_per_unit = tractor.rent_price_per_hour or 0

        driver_required = validated_data.get('driver_required', False)
        driver_charges  = tractor.driver_charges if driver_required else 0
        total_price     = (price_per_unit * quantity) + driver_charges

        booking = Booking.objects.create(
            **validated_data,
            price_per_unit=price_per_unit,
            driver_charges=driver_charges,
            total_price=total_price,
        )
        return booking


class BookingStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Booking
        fields = ['status']
