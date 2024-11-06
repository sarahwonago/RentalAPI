from rest_framework import serializers
from django.contrib.auth import get_user_model

from account.serializers import UserSerializer


from .models import Tenant

User = get_user_model()


class TenantProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the tenant model.
    """

    class Meta:
        model = Tenant
        fields = [
            "id"
        ]



class TenantRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for tenant registration.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "date_joined",
            "role"
        ]


    def create(self, validated_data):
        """
        Create a tenant user.
        """

        # Default password for landlord users.
        default_password = "tpassword123!"

        # create a landlord user with the validated data and role.
        user = User.objects.create_user(
            **validated_data, 
            role=User.TENANT
            )
        
        # sets the default password for landlords and saves the user.
        user.set_password(default_password)
        user.save()


        return user
