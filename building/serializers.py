from rest_framework import serializers
from django.db import IntegrityError

from .models import Building, House

class BuildingSerializer(serializers.ModelSerializer):
    """
    Serializer for the building model.
    """
    class Meta:
        model = Building
        fields = [
            "id",
            "name",
            "address",
            "house_numbers"
        ]

    def create(self, validated_data):
        # perform uniqueness check for building creation
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError("Building with that name for this landlord already exists")
      

    def update(self, instance, validated_data):
        # perform uniqueness check for full updates
        try:
            return super().update(instance, validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError("Building with that name for this landlord already exists")
      
    def validate(self, attrs):
        # perform uniqueness check for partial updates

        landlord = self.context['request'].user
        building_id = self.instance.id if self.instance else None

        if Building.objects.filter(
            landlord=landlord,
            name=attrs.get('name', self.instance.name) #checks name if updated
        ).exclude(id=building_id).exists(): # exclude ensures we dont flag the current building as a duplicate
            raise serializers.ValidationError("Building with that name for this landlord already exists")
        return attrs

class HouseSerializer(serializers.ModelSerializer):
    """
    Serializer for the house model.
    """

    building = serializers.StringRelatedField()

    class Meta:
        model = House
        fields = [
            "id",
            "name",
            "building",
            "rent_amount",
            "default_due_day",
            "is_occupied"
        ]

    def validate_rent_amount(self, value):
        """
        Validate rent amount
        """
        if value <= 0:
            raise serializers.ValidationError("Rent amount must be greater than 0")
        return value