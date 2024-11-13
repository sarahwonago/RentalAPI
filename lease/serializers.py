from rest_framework import serializers

from .models import Lease


class LeaseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Lease model.
    """

    start_date = serializers.DateTimeField(read_only=True)
    account = serializers.CharField(read_only=True)
    tenant = serializers.CharField(source='tenant.username', read_only=True, required=False)
    house = serializers.CharField(source='house.name', read_only=True, required=False)

    class Meta:
        model = Lease
        fields = [
            "id",
            "tenant",
            "house",
            "start_date",
            "end_date",
            "is_active",
            "account"
        ]