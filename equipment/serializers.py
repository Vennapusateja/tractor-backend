# serializers.py
from rest_framework import serializers
from .models import Equipment, EquipmentImage


class EquipmentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = EquipmentImage
        fields = ['id', 'image']


class EquipmentSerializer(serializers.ModelSerializer):
    images = EquipmentImageSerializer(many=True, read_only=True)

    class Meta:
        model  = Equipment
        fields = '__all__'
        read_only_fields = ['id', 'owner', 'created_at']
