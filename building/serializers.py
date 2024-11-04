from rest_framework import serializers

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