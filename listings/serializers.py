from rest_framework import serializers
from .models import Tractor, TractorImage
from users.serializers import UserSerializer


class TractorImageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TractorImage
        fields = ['id', 'image', 'is_cover', 'order']


class TractorSerializer(serializers.ModelSerializer):
    images     = TractorImageSerializer(many=True, read_only=True)
    owner      = UserSerializer(read_only=True)
    avg_rating = serializers.FloatField(read_only=True)

    class Meta:
        model  = Tractor
        fields = [
            'id', 'owner', 'brand', 'model_name', 'hp', 'year', 'fuel_type',
            'description', 'rent_price_per_hour', 'rent_price_per_acre',
            'sell_price', 'status', 'driver_available', 'driver_charges',
            'location', 'state', 'district', 'pincode', 'latitude', 'longitude',
            'images', 'avg_rating', 'is_active', 'created_at',
        ]
        read_only_fields = ['id', 'owner', 'avg_rating', 'created_at']


class TractorWriteSerializer(serializers.ModelSerializer):
    """Used for create/update — owner is set from request.user"""
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model  = Tractor
        fields = [
            'brand', 'model_name', 'hp', 'year', 'fuel_type', 'description',
            'rent_price_per_hour', 'rent_price_per_acre', 'sell_price',
            'status', 'driver_available', 'driver_charges',
            'location', 'state', 'district', 'pincode', 'latitude', 'longitude',
            'uploaded_images',
        ]

    def create(self, validated_data):
        images = validated_data.pop('uploaded_images', [])
        tractor = Tractor.objects.create(**validated_data)
        for i, img in enumerate(images):
            TractorImage.objects.create(tractor=tractor, image=img, is_cover=(i == 0), order=i)
        return tractor

    def update(self, instance, validated_data):
        images = validated_data.pop('uploaded_images', [])
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        for i, img in enumerate(images):
            TractorImage.objects.create(tractor=instance, image=img, order=i)
        return instance
