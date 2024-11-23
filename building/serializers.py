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
            "house_numbers",
        ]

    def validate(self, attrs):
        """
        Ensure no duplicate building name exists for the landlord.
        """
        landlord = self.context["request"].user
        building_id = self.instance.id if self.instance else None

        # Check for duplicates
        if Building.objects.filter(
            landlord=landlord,
            name=attrs.get("name", self.instance.name if self.instance else None)
        ).exclude(id=building_id).exists():
            raise serializers.ValidationError({"name": "Building with this name already exists for this landlord."})

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
        ]

    def validate_rent_amount(self, value):
        """
        Ensure rent amount is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Rent amount must be greater than 0.")
        return value

    def validate(self, attrs):
        """
        Ensure no duplicate house name exists within the same building.
        """
        building = self.context["view"].kwargs.get("building_id")
        house_id = self.instance.id if self.instance else None

        # Check for duplicates
        if House.objects.filter(
            building=building,
            name=attrs.get("name", self.instance.name if self.instance else None)
        ).exclude(id=house_id).exists():
            raise serializers.ValidationError({"name": "House with this name already exists in the selected building."})

        return attrs
