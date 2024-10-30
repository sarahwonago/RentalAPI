from rest_framework.serializers import ModelSerializer

from .models import Building

class BuildingSerializer(ModelSerializer):
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