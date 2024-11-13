from rest_framework import serializers

from .models import Lease


class LeaseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Lease model.
    """

    start_date = serializers.DateTimeField(read_only=True)
    account = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)

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