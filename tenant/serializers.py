from rest_framework import serializers

from account.serializers import UserSerializer

from .models import Tenant

class TenantSerializer(serializers.ModelSerializer):
    """
    Serializer for the tenant model.
    """

    tenant = UserSerializer()
    house = serializers.StringRelatedField()
    landlord = serializers.StringRelatedField()

    class Meta:
        model = Tenant
        fields = [
            "id",
            "tenant",
            "house",
            "landlord"
        ]