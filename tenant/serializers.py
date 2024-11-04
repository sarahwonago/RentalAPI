from rest_framework import serializers
from django.contrib.auth import get_user_model

from account.serializers import UserSerializer


from .models import Tenant

User = get_user_model()


class TenantSerializer(serializers.ModelSerializer):
    """
    Serializer for the tenant model.
    """

    tenant = UserSerializer()
    landlord = serializers.StringRelatedField(required=False)

    class Meta:
        model = Tenant
        fields = [
            "id",
            "tenant",
            "house",
            "landlord"
        ]
