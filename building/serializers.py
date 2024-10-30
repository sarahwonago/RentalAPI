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
            "rent_due_date",
            "is_occupied"
        ]